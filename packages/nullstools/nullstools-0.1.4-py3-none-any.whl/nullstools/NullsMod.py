import zipfile
import os
import shutil
import json
import logging

class Mod:
    def __init__(self, file_path: str):
        """
        Mod - класс для хранения и взаимодействия с вашим модом .nullsmod
        :param file_path: Путь до .nullsmod файла.
        """
        
        if not file_path.endswith(".nullsmod"):
            raise Exception("Файл должен иметь расширение .nullsmod")

        if not os.path.exists(".nullstools"):
            os.mkdir(".nullstools")

        if os.path.exists(f".nullstools/{file_path}"):
            shutil.rmtree(f".nullstools/{file_path}")



        with zipfile.ZipFile(file_path) as file:
            file.extractall(f".nullstools/{file_path}")

        self.path = f".nullstools/{file_path}"


    def build(self, dynamic_module_variant: str = "default"):
        """
        Собирает ваш мод в .zip/.json файл для подписи.

        :param dynamic_module_variant: Вариант сборки мода. Уточняется в документации к моду.

        :return: Путь до собранного файла.
        """
        temp_json = {} # Файл сборки

        with open(f"{self.path}/content.json") as f:
            main = json.load(f)
        logging.info("Главный файл загружен")


        build = main[main["mod"]["build_config"]]
        logging.info("Build-конфиг загружен")


        temp_json = build["meta-info"]

        packets = build["packets"]
        dynamic_modules = build["dynamic_modules"]
        logging.info("Данные build загружены")

        for dynamic_module in dynamic_modules:
            logging.info(f"Найден динамический модуль: {dynamic_module}")
            with open(f"{self.path}/{dynamic_module['file']}") as f:
                dynamic_module_file = json.load(f)

            dynamic_module_variant_mod = dynamic_module_file[
                dynamic_module["default_module"] if dynamic_module_variant == "default" else dynamic_module_variant
            ]

            if dynamic_module_variant_mod["used_packets"] is not None:

                for packet in dynamic_module_variant_mod["used_packets"]:
                    logging.info("Обнаружен используемый сторонний пакет")
                    packet = packet.split(".")

                    with open(f"{self.path}/{packets[packet[0]]}") as f:
                        tmp_packet = json.load(f)
                    try:
                        temp_json[packet[1]].update(tmp_packet[packet[1]][packet[2]])
                    except KeyError:
                        temp_json[packet[1]] = tmp_packet[packet[1]][packet[2]]

            if dynamic_module["type"] == "root":
                logging.info("Запись динамического модуля в корень...")
                temp_json.update(dynamic_module_variant_mod["mod_objects"])

            else:
                logging.info(f"Запись динамического модуля в {dynamic_module['type']}...")
                temp_json[dynamic_module["type"]] = dynamic_module_variant_mod["mod_objects"]

        if os.path.exists(".nullstools/temp"):
            shutil.rmtree(".nullstools/temp")

        os.mkdir(".nullstools/temp")

        if main["mod"]["mod"] != [None]:
            for mod in main["mod"]["mod"]:
                with open(f"{self.path}/{main['mod']['mod']}") as f:
                    temp_json.update(json.load(f))
            logging.info("json-файлы объеденены.")

        with open(".nullstools/temp/result.json", "w") as f:
            json.dump(temp_json, f)

        with zipfile.ZipFile("result.zip", "w") as f:
            f.write(".nullstools/temp/result.json", "content.json")
            logging.info(".json загружен в архив")

            if main["mod"]["icon"] is not None:
                f.write(f"{self.path}/{main['mod']['icon']}", "icon.png")
                logging.info("Иконка загружена в архив")

            if main["mod"]["assets_path"] is not None:
                for file in os.listdir(f"{self.path}/{main['mod']['assets_path']}"):
                    f.write(file)

            logging.info("Файл собран.")


        return "result.zip"










        
        
