import json

class OCRElement(object):
    def __init__(self, content, left_top_x, left_top_y, width, height, tags=None):
        self.content = content
        self.leftTopX = left_top_x
        self.leftTopY = left_top_y
        self.width = width
        self.height = height
        self.tags = tags if tags is not None else {}
        self.bbox = ((0, 0), (0, 0))

    @classmethod
    def from_dict(cls, data_dict):
        """
        Create an OCRElement instance from a dictionary.
        :param data_dict: Dictionary containing element properties.
        :return: OCRElement instance.
        """
        content = data_dict.get('text', '')
        left_top_x = data_dict['rect'].get('x', 0)
        left_top_y = data_dict['rect'].get('y', 0)
        width = data_dict['rect'].get('width', 0)
        height = data_dict['rect'].get('height', 0)
        tags = {'confidence': data_dict.get('confidence', 1)}
        
        return cls(content, left_top_x, left_top_y, width, height, tags)

    def analyze_content(self):
        pass

    def center(self):
        return self.leftTopX + self.width / 2, self.leftTopY + self.height / 2

    def left(self):
        return self.leftTopX + 20, self.leftTopY + self.height / 2

    def right(self):
        return self.leftTopX + self.width - 20, self.leftTopY + self.height / 2

    def top(self):
        return self.leftTopX + self.width / 2, self.leftTopY + 10

    def bottom(self):
        return self.leftTopX + self.width / 2, self.leftTopY + self.height - 10

    def __str__(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def to_dict(self, index=None):
        """Convert the Element instance to a dictionary. Optionally add an ID."""
        element_dict = {
            'content': self.content,
            'leftTopX': self.leftTopX,
            'leftTopY': self.leftTopY,
            'width': self.width,
            'height': self.height,
            'tags': self.tags
        }
        if index is not None:
            element_dict['id'] = index
            element_dict['indexId'] = index
        return element_dict

    def add_tag(self, tag):
        new_tags = self.tags.copy()
        new_tags.update(tag)
        self.tags = new_tags

    def is_location(self):
        return 'location' in self.tags


if __name__ == '__main__':

    # Example usage with JSON data:
    json_data = [{"confidence":0.30000001192092896,"text":"19:28","rect":{"y":22,"height":23.999999999999915,"width":75,"x":40.000000939999978}},{"rect":{"y":81.722601802605368,"width":98.145729064941406,"height":26.554796218872099,"x":95.927136283710752},"text":"搂瞱神器","confidence":0.5},{"rect":{"x":92.000000254545455,"y":137.99999990000015,"width":56,"height":30},"text":"推荐","confidence":1},{"rect":{"width":50.000000000000007,"height":25.999999999999943,"x":24.000000499999988,"y":139.99999986000012},"text":"关注","confidence":1},{"text":"1元","rect":{"x":45.999999620000011,"y":189.99999974000002,"width":46,"height":25.999999999999943},"confidence":0.5},{"text":"起拍","confidence":0.5,"rect":{"height":25.999999999999943,"y":214.00000021666665,"x":44.000000283333335,"width":46}},{"rect":{"y":251.32665050091134,"height":25.346698760986328,"width":86.366058349609361,"x":23.816971301170501},"text":"阿里拍卖","confidence":1},{"rect":{"width":120,"y":316.00000009999997,"height":25.999999999999943,"x":27.999999142857153},"confidence":0.5,"text":"淘宝直播证"},{"rect":{"height":25.999999999999943,"y":140.00000018571427,"width":74,"x":168.00000044285713},"confidence":1,"text":"小时达"},{"rect":{"width":92.245681762695341,"x":263.87715835082884,"y":137.5909444166623,"height":28.818111419677734},"confidence":1,"text":"百亿加补"},{"text":"国家补贴","confidence":1,"rect":{"height":28.265434265136662,"y":137.86728299855145,"width":94.078720092773423,"x":377.96063916990647}},{"confidence":1,"text":"搜索","rect":{"height":32.000000000000028,"x":489.99999968888892,"y":80.000000111111149,"width":56.000000000000021}},{"confidence":0.30000001192092896,"rect":{"y":139.99999986000012,"height":25.999999999999943,"x":492.00000055999999,"width":56.000000000000021},"text":"穿招"},{"rect":{"width":24.000000000000018,"y":144.00000008000006,"x":551.99999976000004,"height":15.999999999999943},"confidence":0.30000001192092896,"text":"V"},{"rect":{"height":24.000000000000057,"x":136.00000067999997,"y":251.99999988000013,"width":68},"text":"淘工厂","confidence":1},{"confidence":1,"rect":{"width":86.046173095703139,"height":24.165988922119084,"y":251.91700571083754,"x":229.97691369467418},"text":"芭芭农场"},{"text":"领淘金币","rect":{"width":86.000000000000014,"x":331.9999994625,"y":252.00000010000008,"height":24.000000000000057},"confidence":0.5},{"rect":{"x":222.00000158,"height":27.999999999999972,"y":315.99999988000002,"width":158.00000000000003},"text":"百亿补贴 领国补","confidence":0.5},{"rect":{"y":253.89177999489243,"x":436.46468983676272,"width":83.570472717285227,"height":20.296322822570687},"text":"红包签到","confidence":0.30000001192092896},{"rect":{"x":535.99999966249993,"y":252.00000010000008,"height":24.000000000000057,"width":54.000000000000007},"text":"天猫走","confidence":0.5},{"rect":{"x":415.9999988714286,"y":316.00000009999997,"height":25.999999999999943,"width":158},"confidence":0.5,"text":"淘宝秒杀 限时抢"},{"text":"薈菇来了","confidence":0.30000001192092896,"rect":{"height":22.539540290832463,"y":487.7302304275604,"x":25.922786169092426,"width":76.154426574707031}},{"confidence":0.30000001192092896,"rect":{"width":80,"y":546.00000011999998,"x":51.999999200000019,"height":24.000000000000057},"text":"天天满減"},{"rect":{"x":239.82547728582017,"width":50.349044799804673,"height":22.805266380310059,"y":485.59736739411642},"text":"¥234","confidence":0.5},{"rect":{"height":26.000000000000085,"y":546.00000021666665,"x":145.99999890000004,"width":212},"text":"你有3张满减券待使用","confidence":0.5},{"confidence":0.5,"text":"¥59.9","rect":{"width":56.000000000000021,"x":428.00000025714286,"y":486.00000018571427,"height":26.000000000000085}},{"text":"秘杀价","confidence":0.30000001192092896,"rect":{"width":49.999999999999986,"y":487.99999981999997,"height":17.999999999999972,"x":503.99999989999992}},{"rect":{"y":546.00000013333329,"x":436.99999880000001,"height":24.000000000000057,"width":128.99999999999991},"text":"75 立即使用","confidence":0.30000001192092896},{"rect":{"y":648.47457751042748,"height":53.365158081054602,"x":62.621955123770022,"width":177.49125671386722},"confidence":0.30000001192092896,"text":"*买二兔二"},{"rect":{"height":39.561090469360352,"y":696.69230514048854,"width":118.02262115478516,"x":77.058823366755234},"text":"質2189","confidence":0.30000001192092896},{"text":"畅游多地","rect":{"y":698.00000012222222,"x":349.999999,"height":53.999999999999915,"width":180},"confidence":1},{"rect":{"y":760.00000017999992,"width":164.00000000000003,"height":17.999999999999972,"x":357.99999955999999},"confidence":0.30000001192092896,"text":"长芯防空莎行天下经济酸两办云"},{"confidence":1,"text":"【官方直营】皇家加勒比光","rect":{"width":239.99999999999997,"y":891.99999990000003,"x":24.000001499999968,"height":23.999999999999915}},{"confidence":0.5,"text":"¥2,323","rect":{"y":927.2355081944213,"width":82.584503173828125,"height":33.528984069824332,"x":21.707748374513905}},{"text":"已售2000+","confidence":0.30000001192092896,"rect":{"y":934.00000010000008,"x":109.99999920000002,"width":96,"height":20}},{"confidence":1,"rect":{"x":313.99999870000005,"y":892.00000008888878,"width":234.00000000000009,"height":24.000000000000057},"text":"长龙航空龙行天下经济舱"},{"rect":{"x":312.00000108571436,"height":20,"y":925.99999991428581,"width":151.99999999999997},"text":"温宝秒杀 全网低价","confidence":0.5},{"rect":{"x":309.99999836000006,"width":164.00000000000003,"y":960.00000016000013,"height":23.999999999999915},"confidence":0.5,"text":"¥366 已售2000+"},{"text":"投资金条","confidence":0.5,"rect":{"width":150.31039428710935,"x":121.8448030398992,"y":1003.3778359544556,"height":39.244325637817354}},{"text":"淘","rect":{"height":32.000000000000028,"x":40.000000180000001,"y":1185.9999999000001,"width":36},"confidence":0.30000001192092896},{"confidence":0.5,"text":"视频","rect":{"x":159.99999973333334,"height":17.999999999999972,"width":32,"y":1212.0000000833334}},{"text":"消息","confidence":0.30000001192092896,"rect":{"y":1211.9999999000001,"width":34.000000000000014,"height":18.000000000000114,"x":278.00000033999993}},{"confidence":1,"rect":{"width":49.999999999999986,"height":20,"x":390.00000041666669,"y":1209.9999999000001},"text":"购物车"},{"rect":{"x":497.93460400405638,"width":64.130790710449276,"y":1209.7646351813446,"height":18.470730781555176},"text":"我的润宝","confidence":0.5}]

    ocr_elements = [OCRElement.from_dict(data) for data in json_data]

    print(json.dumps([OCRElement.to_dict(element) for element in ocr_elements], indent=4, ensure_ascii=False))