class CleanItemPipeline:
    def process_item(self, item, spider):
        if "availability" in item and isinstance(item["availability"], str):
            item["availability"] = " ".join(item["availability"].split())
        if "price" in item and isinstance(item["price"], str):
            value = item["price"].replace("£", "").strip()
            try:
                item["price_numeric"] = float(value)
            except ValueError:
                pass
        if "tags" in item and isinstance(item["tags"], list):
            item["tags"] = sorted(item["tags"])
        return item
