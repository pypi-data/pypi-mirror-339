from loguru import logger
from typing import Dict, List, Any

from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V5

from p1_influx_db.dsmr_parse import dsmrParse, p1Messages

from p1_influx_db.mqtt import Client


def read_and_publish_p1(telegram, dsmrParser: dsmrParse, client: Client, dead_queue: List[p1Messages]):
    info_list = dsmrParser.parse_dsmr_telegram(telegram)
    for dsmr_message in info_list:
        try:
            client.publish_messages(dsmr_message)
        except RuntimeError as e:
            logger.error(f"Runtime error: {e}")
            dead_queue.append(dsmr_message)
    loop_dead_queue = dead_queue.copy()
    for message in loop_dead_queue:
        try:
            error = False
            client.publish_messages(message)
        except RuntimeError as e:
            error = True
            logger.error(f"Runtime error: {e}")
        finally:
            if not error:
                dead_queue.remove(message)
    return dead_queue


def mqttmain(config: Dict[str, Any]):
    logger.info("Opening SerialReader")
    mqtt_config = config["mqtt"]
    dsmrParser = dsmrParse(config["p1"])
    client = Client(**mqtt_config)
    client.start()
    serial_reader = SerialReader(
        device=config["p1"]["device"],
        serial_settings=SERIAL_SETTINGS_V5,
        telegram_specification=telegram_specifications.V5,
    )
    dead_queue = []
    try:
        for telegram in serial_reader.read_as_object():
            dead_queue = read_and_publish_p1(telegram, dsmrParser, client, dead_queue)
            if len(dead_queue) > 2000:
                raise RuntimeError("Dead queue is larger than 2000")
    except Exception as e:
        client.stop()
        logger.info("Closing MqttClient")
        raise e
