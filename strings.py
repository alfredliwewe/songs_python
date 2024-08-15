class Strings:
    @staticmethod
    def implode(glue:str, values:list):
        result = ""
        for row in values:
            if result == "":
                result = str(row)
            else:
                result += glue+str(row)
        return result