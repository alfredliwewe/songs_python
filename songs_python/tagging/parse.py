class TitleParser:
    def __init__(self, title):
        self.title = str(title).lower()

    def multipleContains(self, text, chars):
        text = str(text)
        result = False
        for char in chars:
            if text.__contains__(char):
                result = True

        return result

    def splitByMultiple(self, stmt, words):
        res = [stmt]

        for word in words:
            new = []
            for s in res:
                new = new + s.split(word)
            res = new
        return res



    def getParts(self):
        first = self.title
        last = ""
        chars = [" ft ", " feat ", " featuring ", " ft. ", " feat. ", " x "]
        if self.multipleContains(self.title, chars):
            done = False;

            for c in chars:
                if not done:
                    if self.title.__contains__(c):
                        done = True
                        parts = self.title.split(c)
                        if len(parts) > 1:
                            first = parts[0]
                            last = parts[1]

        return [first, last]

    def cutBetween(self, string, o, f):
        res = ""
        can = False

        for letter in str:
            if letter == f:
                can = False

            if can:
                res = res + letter

            if letter == o:
                can = True
                pass

        return res.strip()


    def getFeaturedArtists(self):
        left = ""
        parts = self.getParts()
        if parts[1] != "":
            if str(parts[1]).__contains__("("):
                position = str(parts[1]).index("(")
                left = str(parts[1])[0:position]
            elif str(parts[1]).__contains__("["):
                position = str(parts[1]).index("[")
                left = str(parts[1])[0:position]
            else:
                left = parts[1]

            artitsts = self.splitByMultiple(left, [", ", " x ", " and ", " & "])
            return artitsts
        else:
            return []

    def getProducers(self):
        parts = self.getParts()
        if parts[1] != "":
            left = ""
            part1 = str(parts[1])
            if part1.__contains__("("):
                position = part1.index("(")
                if part1.__contains__(")"):
                    last = part1.index(")")
                    left = part1[position:last]
            elif part1.__contains__("["):
                position = part1.index("[")
                if part1.__contains__("]"):
                    last = part1.index("]")
                    left = part1[position:last]

            if left == "":
                return []
            else:
                left = self.replaceAll(str(left), ["[", "]", "(", ")", "prod. ", "prod ", "produced by "])
                return self.splitByMultiple(left, [", ", " x ", " and ", " & "])
        else:
            return []

    def replaceAll(self, left, param):
        for p in param:
            left = left.replace(p, "")
        return left.strip()