import requests as rq
from xml.etree import ElementTree
from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass


class Category:
    class Display:
        def __init__(self, page: str, menu: str):
            self.page = page
            self.menu = menu

    class PublicInterval:
        def __init__(self, start: str, end: str):
            self.start = start
            self.end = end

    class NotVisibleInLanguage:
        def __init__(self, language: str):
            self.language = language

    class PageLayout:
        def __init__(self, category_list: int, product_list: int):
            self.category_list = category_list
            self.product_list = product_list

    class Parent:
        def __init__(self, id: int, tree: str):
            self.id = id
            self.tree = tree

    @dataclass
    class Products:
        all: int
        new: int

    class Texts:
        def __init__(self, top: str, bottom: str, menu: str):
            self.top = top
            self.bottom = bottom
            self.menu = menu

    class Meta:
        def __init__(self, keywords: str, description: str, title: str, robots: str):
            self.keywords = keywords
            self.description = description
            self.title = title
            self.robots = robots

    class AutomaticMeta:
        def __init__(self, keywords: str, description: str, title: str):
            self.keywords = keywords
            self.description = description
            self.title = title

    class Image:
        def __init__(self, url: str, og: str):
            self.url = url
            self.og = og

    class Tags:
        def __init__(self, tag: str):
            self.tag = tag

    class HistoryEvent:
        def __init__(self, action: str, time: datetime, id: int):
            self.action = action
            self.time = time
            self.id = id

    class History:
        def __init__(self, events: List["Category.HistoryEvent"]):
            self.events = events

    def __init__(
        self,
        action: str,
        state: Optional[str],
        id: int,
        name: str,
        url: Optional[str],
        sef_url: str,
        alt_url: Optional[str],
        alt_url_blank: Optional[str],
        display: Display,
        disable_filter: Optional[str],
        public_interval: Optional[PublicInterval],
        not_visible_in_language: Optional[NotVisibleInLanguage],
        page_layout: Optional[PageLayout],
        parent: Optional[Parent],
        order: Optional[int],
        products: Optional[Products],
        texts: Optional[Texts],
        meta: Optional[Meta],
        automatic_meta: Optional[AutomaticMeta],
        create_time: Optional[int],
        last_mod_time: Optional[int],
        image: Optional[Image],
        tags: Optional[Tags],
        history: Optional[History],
    ):
        self.action = action
        self.state = state
        self.id = id
        self.name = name
        self.url = url
        self.sef_url = sef_url
        self.alt_url = alt_url
        self.alt_url_blank = alt_url_blank
        self.display = display
        self.disable_filter = disable_filter
        self.public_interval = public_interval
        self.not_visible_in_language = not_visible_in_language
        self.page_layout = page_layout
        self.parent = parent
        self.order = order
        self.products = products
        self.texts = texts
        self.meta = meta
        self.automatic_meta = automatic_meta
        self.create_time = create_time
        self.last_mod_time = last_mod_time
        self.image = image
        self.tags = tags
        self.history = history

    def __repr__(self):
        return f"<Category(action={self.action}, state={self.state}, id={self.id}, name={self.name}, url={self.url}, sef_url={self.sef_url}, alt_url={self.alt_url}, alt_url_blank={self.alt_url_blank}, display={self.display}, disable_filter={self.disable_filter}, public_interval={self.public_interval}, not_visible_in_language={self.not_visible_in_language}, page_layout={self.page_layout}, parent={self.parent}, order={self.order}, products={self.products}, texts={self.texts}, meta={self.meta}, automatic_meta={self.automatic_meta}, create_time={self.create_time}, last_mod_time={self.last_mod_time}, image={self.image}, tags={self.tags}, history={self.history})>"


from enum import Enum
from typing import List, Optional


class Action(Enum):
    ADD = "add"
    MODIFY = "modify"
    DELETE = "delete"


class State(Enum):
    LIVE = "live"
    DELETED = "deleted"


class HistoryEventAction(Enum):
    ADD = "add"
    MODIFY = "modify"
    DELETE = "delete"


class StatusType(Enum):
    BASE = "base"
    PLUS = "plus"


class StatusValue(Enum):
    VALUE_0 = 0
    VALUE_1 = 1


class YesNo(Enum):
    YES = "yes"
    NO = "no"
    ONLY = "only"


class Point(Enum):
    DEFAULT = "default"
    NO = "no"
    POINT = "point"


class PriceType(Enum):
    NORMAL = "normal"
    SALE = "sale"
    SPECIAL = "special"


class DiscountType(Enum):
    AMOUNT_FIX = "amount_fix"
    AMOUNT_DISCOUNT = "amount_discount"
    PERCENT = "percent"


class CategoryType(Enum):
    BASE = "base"
    ALT = "alt"


class ImageType(Enum):
    BASE = "base"
    ALT = "alt"


class ContentType(Enum):
    MINIMAL = "minimal"
    SHORT = "short"
    NORMAL = "normal"
    FULL = "full"


class ParamType(Enum):
    TEXT = "text"
    TEXTMORE = "textmore"
    ENUM = "enum"
    ENUMMORE = "enummore"
    NUM = "num"
    INTERVAL = "interval"
    COLOR = "color"
    LINK = "link"  # Valós URL lehet a paraméter értéke (pl.: https://unas.hu)
    LINKBLANK = "linkblank"  # Link, új ablakban megnyitva. Valós URL lehet a paraméter értéke (pl.: https://unas.hu)
    LINK_TEXT = "link_text"  # Szöveges link. Valós URL és egy hozzátartozó szöveg lehet a paraméter értéke (pl.: https://unas.hu - Unas kezdőoldal)
    HTML = "html"  # Értéke HTML tartalom
    ICON = "icon"  # Az áruházba előre feltöltött ikon sorszámát veheti fel (pl.: 3)
    ICONMORE = "iconmore"  # Ikon, többértékű. Több előre feltöltött ikon sorszámát veheti fel értékként, vesszővel elválasztva (pl.: 1,2,3)
    PIC = "pic"  # Kép (pl.: https://unas.hu/image.jpg)
    PICLINK = "piclink"  # Kép fájlkezelőből
    PICLINKTEXT = "piclinktext"  # Kép fájlkezelőből alternatív szöveggel
    DATE = "date"  # Dátum, az áruházban kezelhető nap típusok értékével megadva (pl.: 10|day). A pipe karakter utáni lehetséges értékek: day, day_except_weekend, day_except_holidays, day_except_weekend_and_holidays
    CUST_INPUT_TEXT = "cust_input_text"  # Vásárló által megadható szövegbeviteli mező a termék részletek oldalon
    CUST_INPUT_SELECT = "cust_input_select"  # Vásárló által kiválasztható Legördülő menü a termék részletek oldalon
    CUST_INPUT_FILE = "cust_input_file"  # Vásárló által megadható fájlfeltöltő mező a termék részletek oldalon


class Product:
    class HistoryEvent:
        def __init__(
            self,
            action: HistoryEventAction,
            time: int,
            sku: str,
            sku_old: Optional[str] = None,
        ):
            self.action = action
            self.time = time
            self.sku = sku
            self.sku_old = sku_old

    class History:
        def __init__(self, events: List["Product.HistoryEvent"]):
            self.events = events

    class Status:
        def __init__(self, type: StatusType, value: StatusValue, name: Optional[str] = None, id: Optional[str] = None):
            self.type = type
            self.value = value
            self.name = name
            self.id = id

    class Description:
        def __init__(self, short: str, long: str):
            self.short = short
            self.long = long

    class Price:
        def __init__(
            self,
            type: PriceType,
            net: float,
            gross: float,
            start: Optional[str] = None,
            end: Optional[str] = None,
        ):
            self.type = type
            self.net = net
            self.gross = gross
            self.start = start
            self.end = end

    class Prices:
        def __init__(
            self, appearance: str, vat: Optional[str], price: Optional["Product.Price"]
        ):
            self.appearance = appearance
            self.vat = vat
            self.price = price

    class QtyDiscountStep:
        def __init__(
            self,
            lower: int,
            upper: int,
            price: Optional[float] = None,
            discount: Optional[float] = None,
        ):
            self.lower = lower
            self.upper = upper
            self.price = price
            self.discount = discount

    class QtyDiscount:
        def __init__(
            self, discount_type: DiscountType, steps: List["Product.QtyDiscountStep"]
        ):
            self.discount_type = discount_type
            self.steps = steps

    @dataclass
    class Category:
        type: CategoryType
        id: Optional[int]
        name: Optional[str]

    class Image:
        def __init__(
            self,
            type: ImageType,
            filename: str,
            alt: str,
            sef_url: Optional[str] = None,
        ):
            self.type = type
            self.filename = filename
            self.alt = alt
            self.sef_url = sef_url

    @dataclass
    class Param:
        id: int
        type: ParamType
        name: str
        group: str
        value: str
        before: Optional[str]
        after: Optional[str]

    def __init__(
        self,
        action: "Action",
        state: Optional["State"] = None,
        id: Optional[int] = None,
        sku: str = "",
        name: Optional[str] = None,
        unit: Optional[str] = None,
        minimum_qty: Optional[float] = None,
        maximum_qty: Optional[float] = None,
        alert_qty: Optional[float] = None,
        unit_step: Optional[float] = None,
        alter_unit_qty: Optional[float] = None,
        alter_unit_unit: Optional[float] = None,
        weight: Optional[float] = None,
        point: Optional["Point"] = None,
        buyable_with_point: Optional["YesNo"] = None,
        description: Optional["Product.Description"] = None,
        prices: Optional["Product.Prices"] = None,
        qty_discount: Optional["Product.QtyDiscount"] = None,
        categories: Optional[List["Product.Category"]] = None,
        images: Optional[List["Product.Image"]] = None,
        params: Optional[List["Product.Param"]] = None,
        statuses: Optional[List["Product.Status"]] = None,
    ):
        self.action = action
        self.state = state
        self.id = id
        self.sku = sku
        self.name = name
        self.unit = unit
        self.minimum_qty = minimum_qty
        self.maximum_qty = maximum_qty
        self.alert_qty = alert_qty
        self.unit_step = unit_step
        self.alter_unit_qty = alter_unit_qty
        self.alter_unit_unit = alter_unit_unit
        self.weight = weight
        self.point = point
        self.buyable_with_point = buyable_with_point
        self.description = description
        self.prices = prices
        self.qty_discount = qty_discount
        self.categories = categories
        self.images = images
        self.params = params
        self.statuses = statuses

    def __repr__(self):
        return f"<Product(action={self.action}, state={self.state}, id={self.id}, sku={self.sku}, name={self.name}, unit={self.unit}, minimum_qty={self.minimum_qty}, maximum_qty={self.maximum_qty}, alert_qty={self.alert_qty}, unit_step={self.unit_step}, alter_unit_qty={self.alter_unit_qty}, alter_unit_unit={self.alter_unit_unit}, weight={self.weight}, point={self.point}, buyable_with_point={self.buyable_with_point}, description={self.description}, prices={self.prices}, qty_discount={self.qty_discount}, categories={self.categories}, images={self.images}, statuses={self.statuses})>"

    def add_category(self, category: "Product.Category"):
        self.categories.append(category)

    def remove_category(self, category_id: int):
        self.categories = [
            category for category in self.categories if category.id != category_id
        ]


class UnasAPIBase:
    def __init__(self, api_key):
        self.api_key = api_key
        self.token = None

    def get_unas_token(self):
        token_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><ApiKey>{self.api_key}</ApiKey></Params>'
        token_request = rq.get("https://api.unas.eu/shop/login", data=token_payload)
        token_tree = ElementTree.fromstring(token_request.content)
        if token_tree[0].tag == "Token":
            self.token = token_tree[0].text
        return self.token

    def make_request(self, endpoint, payload, method="GET"):
        if not self.token:
            self.get_unas_token()
        headers = {"Authorization": f"Bearer {self.token}"}
        if method == "GET":
            response = rq.get(
                "https://api.unas.eu/shop/" + endpoint,
                headers=headers,
                data=payload.encode("utf-8"),
            )
        elif method == "POST":
            response = rq.post(
                "https://api.unas.eu/shop/" + endpoint,
                headers=headers,
                data=payload.encode("utf-8"),
            )
        if response.status_code != 200:
            raise Exception(
                f"Request failed with status code {response.status_code}. Response: {response.text}"
            )
        return ElementTree.fromstring(response.content)

    def get_unas_feed_url(self, lang="hu"):
        url_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><Format>xlsx</Format><Lang>{lang}</Lang></Params>'
        url_request = self.make_request("getProductDB", url_payload)
        url = url_request[0].text
        return url

    def get_category(self, category_id: int) -> Category:
        payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><Id>{category_id}</Id></Params>'
        response = self.make_request("getCategory", payload)
        category_tree = response.find(".//Category")

        # Parse the XML response into the Category data structure
        category = Category(
            action=None,
            state=category_tree.findtext("State"),
            id=int(category_tree.findtext("Id")),
            name=category_tree.findtext("Name"),
            url=category_tree.findtext("Url"),
            sef_url=category_tree.findtext("SefUrl"),
            alt_url=category_tree.findtext("AltUrl"),
            alt_url_blank=category_tree.findtext("AltUrlBlank"),
            display=Category.Display(
                page=category_tree.findtext("Display/Page"),
                menu=category_tree.findtext("Display/Menu"),
            ),
            disable_filter=category_tree.findtext("DisableFilter"),
            public_interval=(
                Category.PublicInterval(
                    start=category_tree.findtext("PublicInterval/Start"),
                    end=category_tree.findtext("PublicInterval/End"),
                )
                if category_tree.find("PublicInterval") is not None
                else None
            ),
            not_visible_in_language=(
                Category.NotVisibleInLanguage(
                    language=category_tree.findtext("NotVisibleInLanguage/Language")
                )
                if category_tree.find("NotVisibleInLanguage") is not None
                else None
            ),
            page_layout=(
                Category.PageLayout(
                    category_list=(
                        int(category_tree.findtext("PageLayout/CategoryList"))
                        if category_tree.findtext("PageLayout/CategoryList") is not None
                        else None
                    ),
                    product_list=(
                        int(category_tree.findtext("PageLayout/ProductList"))
                        if category_tree.findtext("PageLayout/ProductList") is not None
                        else None
                    ),
                )
                if category_tree.find("PageLayout") is not None
                else None
            ),
            parent=(
                Category.Parent(
                    id=(
                        int(category_tree.findtext("Parent/Id"))
                        if category_tree.findtext("Parent/Id") is not None
                        else None
                    ),
                    tree=category_tree.findtext("Parent/Tree"),
                )
                if category_tree.find("Parent") is not None
                else None
            ),
            order=(
                int(category_tree.findtext("Order"))
                if category_tree.findtext("Order") is not None
                else None
            ),
            products=(
                Category.Products(
                    all=(
                        int(category_tree.findtext("Products/All"))
                        if category_tree.findtext("Products/All") is not None
                        else None
                    ),
                    new=(
                        int(category_tree.findtext("Products/New"))
                        if category_tree.findtext("Products/New") is not None
                        else None
                    ),
                )
                if category_tree.find("Products") is not None
                else None
            ),
            texts=(
                Category.Texts(
                    top=category_tree.findtext("Texts/Top"),
                    bottom=category_tree.findtext("Texts/Bottom"),
                    menu=category_tree.findtext("Texts/Menu"),
                )
                if category_tree.find("Texts") is not None
                else None
            ),
            meta=(
                Category.Meta(
                    keywords=category_tree.findtext("Meta/Keywords"),
                    description=category_tree.findtext("Meta/Description"),
                    title=category_tree.findtext("Meta/Title"),
                    robots=category_tree.findtext("Meta/Robots"),
                )
                if category_tree.find("Meta") is not None
                else None
            ),
            automatic_meta=(
                Category.AutomaticMeta(
                    keywords=category_tree.findtext("AutomaticMeta/Keywords"),
                    description=category_tree.findtext("AutomaticMeta/Description"),
                    title=category_tree.findtext("AutomaticMeta/Title"),
                )
                if category_tree.find("AutomaticMeta") is not None
                else None
            ),
            create_time=(
                int(category_tree.findtext("CreateTime"))
                if category_tree.findtext("CreateTime") is not None
                else None
            ),
            last_mod_time=(
                int(category_tree.findtext("LastModTime"))
                if category_tree.findtext("LastModTime") is not None
                else None
            ),
            image=(
                Category.Image(
                    url=category_tree.findtext("Image/Url"),
                    og=category_tree.findtext("Image/OG"),
                )
                if category_tree.find("Image") is not None
                else None
            ),
            tags=(
                Category.Tags(tag=category_tree.findtext("Tags/Tag"))
                if category_tree.find("Tags") is not None
                else None
            ),
            history=(
                Category.History(
                    events=[
                        Category.HistoryEvent(
                            action=event.findtext("Action"),
                            time=datetime.fromtimestamp(int(event.findtext("Time"))),
                            id=int(event.findtext("Id")),
                        )
                        for event in category_tree.findall("History/Event")
                    ]
                )
                if category_tree.find("History") is not None
                else None
            ),
        )

        return category

    ## TODO: NINCS ELLENŐRVE
    def set_category(self, category: Category):
        payload = f"""<?xml version="1.0" encoding="UTF-8" ?>
        <Params>
            <Action>{category.action}</Action>
            <Id>{category.id}</Id>
            <Name>{category.name}</Name>
            <SefUrl>{category.sef_url}</SefUrl>
            <AltUrl>{category.alt_url}</AltUrl>
            <AltUrlBlank>{category.alt_url_blank}</AltUrlBlank>
            <Display>
                <Page>{category.display.page}</Page>
                <Menu>{category.display.menu}</Menu>
            </Display>
            <DisableFilter>{category.disable_filter}</DisableFilter>
            <PublicInterval>
                <Start>{category.public_interval.start}</Start>
                <End>{category.public_interval.end}</End>
            </PublicInterval>
            <NotVisibleInLanguage>
                <Language>{category.not_visible_in_language.language}</Language>
            </NotVisibleInLanguage>
            <PageLayout>
                <CategoryList>{category.page_layout.category_list}</CategoryList>
                <ProductList>{category.page_layout.product_list}</ProductList>
            </PageLayout>
            <Parent>
                <Id>{category.parent.id}</Id>
                <Tree>{category.parent.tree}</Tree>
            </Parent>
            <Order>{category.order}</Order>
            <Texts>
                <Top>{category.texts.top}</Top>
                <Bottom>{category.texts.bottom}</Bottom>
                <Menu>{category.texts.menu}</Menu>
            </Texts>
            <Meta>
                <Keywords>{category.meta.keywords}</Keywords>
                <Description>{category.meta.description}</Description>
                <Title>{category.meta.title}</Title>
                <Robots>{category.meta.robots}</Robots>
            </Meta>
            <AutomaticMeta>
                <Keywords>{category.automatic_meta.keywords}</Keywords>
                <Description>{category.automatic_meta.description}</Description>
                <Title>{category.automatic_meta.title}</Title>
            </AutomaticMeta>
            <Image>
                <OG>{category.image.og}</OG>
            </Image>
            <Tags>
                <Tag>{category.tags.tag}</Tag>
            </Tags>
        </Params>"""

        response = self.make_request("setCategory", payload)
        return response

    def get_product(self, sku: str, content_type: ContentType) -> Product:
        payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><Sku>{sku}</Sku><ContentType>{content_type}</ContentType></Params>'
        response = self.make_request("getProduct", payload)
        product_tree = response.find(".//Product")

        if product_tree is None:
            raise Exception(f"Product with ID {sku} does not exist.")

        # Parse the XML response into the Product data structure
        product = Product(
            action=None,
            state=product_tree.findtext("State"),
            id=int(product_tree.findtext("Id")),
            sku=product_tree.findtext("Sku"),
            name=product_tree.findtext("Name"),
            unit=product_tree.findtext("Unit"),
            minimum_qty=(
                float(product_tree.findtext("MinimumQty"))
                if product_tree.findtext("MinimumQty") is not None
                else None
            ),
            maximum_qty=(
                float(product_tree.findtext("MaximumQty"))
                if product_tree.findtext("MaximumQty") is not None
                else None
            ),
            alert_qty=(
                float(product_tree.findtext("AlertQty"))
                if product_tree.findtext("AlertQty") is not None
                else None
            ),
            unit_step=(
                float(product_tree.findtext("UnitStep"))
                if product_tree.findtext("UnitStep") is not None
                else None
            ),
            alter_unit_qty=(
                float(product_tree.findtext("AlterUnitQty"))
                if product_tree.findtext("AlterUnitQty") is not None
                else None
            ),
            alter_unit_unit=product_tree.findtext("AlterUnitUnit"),
            weight=(
                float(product_tree.findtext("Weight"))
                if product_tree.findtext("Weight") is not None
                else None
            ),
            point=product_tree.findtext("Point"),
            buyable_with_point=product_tree.findtext("BuyableWithPoint"),
            description=Product.Description(
                short=product_tree.findtext("Description/Short"),
                long=product_tree.findtext("Description/Long"),
            ),
            prices=Product.Prices(
                appearance=product_tree.findtext("Prices/Appearance"),
                vat=product_tree.findtext("Prices/Vat"),
                price=Product.Price(
                    type=product_tree.findtext("Prices/Price/Type"),
                    net=float(product_tree.findtext("Prices/Price/Net")),
                    gross=float(product_tree.findtext("Prices/Price/Gross")),
                    start=product_tree.findtext("Prices/Price/Start"),
                    end=product_tree.findtext("Prices/Price/End"),
                ),
            ),
            qty_discount=(
                Product.QtyDiscount(
                    discount_type=product_tree.findtext("QtyDiscount/DiscountType"),
                    steps=[
                        Product.QtyDiscountStep(
                            lower=int(step.findtext("Lower")),
                            upper=int(step.findtext("Upper")),
                            price=(
                                float(step.findtext("Price"))
                                if step.findtext("Price") is not None
                                else None
                            ),
                            discount=(
                                float(step.findtext("Discount"))
                                if step.findtext("Discount") is not None
                                else None
                            ),
                        )
                        for step in product_tree.findall("QtyDiscount/Steps/Step")
                    ],
                )
                if product_tree.find("QtyDiscount") is not None
                else None
            ),
            categories=[
                Product.Category(
                    type=category.findtext("Type"),
                    id=int(category.findtext("Id")),
                    name=category.findtext("Name"),
                )
                for category in product_tree.findall("Categories/Category")
            ],
            images=[
                Product.Image(
                    type=image.findtext("Type"),
                    filename=image.findtext("Filename"),
                    alt=image.findtext("Alt"),
                    sef_url=image.findtext("SefUrl"),
                )
                for image in product_tree.findall("Images/Image")
            ],
            params=[
                Product.Param(
                    id=int(param.findtext("Id")),
                    type=param.findtext("Type"),
                    name=param.findtext("Name"),
                    group=param.findtext("Group"),
                    value=param.findtext("Value"),
                    before=param.findtext("Before"),
                    after=param.findtext("After"),
                )
                for param in product_tree.findall("Params/Param")
            ],
            statuses=[
                Product.Status(
                    type=status.findtext("Type"),
                    value=status.findtext("Value"),
                    name=status.findtext("Name") or None,
                    id=status.findtext("Id") or None,
                )
                for status in product_tree.findall("Statuses/Status")
            ]
        )

        return product

    def set_product(self, product: Product):
        payload = f'''<?xml version="1.0" encoding="UTF-8" ?><Products>
            <Product>
                <Action>{product.action}</Action>
                {f"<Id>{product.id}</Id>" if product.id is not None else ""}
                {f"<Sku>{product.sku}</Sku>" if product.sku is not None else ""}
                {f"<Name>{product.name}</Name>" if product.name is not None else ""}
                {f"<Unit>{product.unit}</Unit>" if product.unit is not None else ""}
                {f"<MinimumQty>{product.minimum_qty}</MinimumQty>" if product.minimum_qty is not None else ""}
                {f"<MaximumQty>{product.maximum_qty}</MaximumQty>" if product.maximum_qty is not None else ""}
                {f"<AlertQty>{product.alert_qty}</AlertQty>" if product.alert_qty is not None else ""}
                {f"<UnitStep>{product.unit_step}</UnitStep>" if product.unit_step is not None else ""}
                {f"<AlterUnitQty>{product.alter_unit_qty}</AlterUnitQty>" if product.alter_unit_qty is not None else ""}
                {f"<AlterUnitUnit>{product.alter_unit_unit}</AlterUnitUnit>" if product.alter_unit_unit is not None else ""}
                {f"<Weight>{product.weight}</Weight>" if product.weight is not None else ""}
                {f"<Point>{product.point}</Point>" if product.point is not None else ""}
                {f"<BuyableWithPoint>{product.buyable_with_point}</BuyableWithPoint>" if product.buyable_with_point is not None else ""}
                {f"""
                <Description>
                    <Short>{product.description.short}</Short>
                    <Long>{product.description.long}</Long>
                </Description>
                """ if product.description is not None else ""}{f"""
                <Prices>
                    {f'<Appearance>{product.prices.appearance}</Appearance>' if product.prices.appearance is not None else ""}
                    {f'<Vat>{product.prices.vat}</Vat>' if product.prices.vat is not None else ""}
                    <Price>
                        <Type>{product.prices.price.type}</Type>
                        <Net>{product.prices.price.net}</Net>
                        <Gross>{product.prices.price.gross}</Gross>
                        {f"<Start>{product.prices.price.start}</Start>" if product.prices.price.start is not None else ""}
                        {f"<End>{product.prices.price.end}</End>" if product.prices.price.end is not None else ""}
                    </Price>
                </Prices>
                """ if product.prices is not None else ""}
                {f"""
                <QtyDiscount>
                    <DiscountType>{product.qty_discount.discount_type}</DiscountType>
                    <Steps>
                        {''.join(f'<Step><Lower>{step.lower}</Lower><Upper>{step.upper}</Upper><Price>{step.price}</Price><Discount>{step.discount}</Discount></Step>' for step in product.qty_discount.steps)}
                    </Steps>
                </QtyDiscount>
                """ if product.qty_discount is not None else ""}
                {f"""
                <Categories>
                    {''.join(f'<Category><Type>{category.type}</Type><Id>{category.id}</Id><Name>{category.name}</Name></Category>' for category in product.categories)}
                </Categories>
                """ if product.categories is not None else ""}
                {f"""
                <Images>
                    {''.join(f'<Image><Type>{image.type}</Type><Filename>{image.filename}</Filename><Alt>{image.alt}</Alt><SefUrl>{image.sef_url}</SefUrl></Image>' for image in product.images)}
                </Images>
                """ if product.images is not None else ""}
                {f"""
                <Params>
                    {''.join(f'<Param><Id>{param.id}</Id><Type>{param.type}</Type><Name><![CDATA[{param.name}]]></Name><Group>{param.group}</Group><Value><![CDATA[{param.value}]]></Value></Param>' for param in product.params)}
                </Params>
                 """ if product.params is not None else "" }
                {f"""
                <Statuses>
                    {''.join(f'<Status><Type><![CDATA[{status.type}]]></Type><Value><![CDATA[{status.value}]]></Value>{f"<Name>{status.name}</Name>" if status.name else ""}{f"<Id>{status.id}</Id>" if status.id else ""}</Status>' for status in product.statuses)}
                </Statuses>
                """ if product.statuses is not None else ""}
            </Product>
        </Products>
        '''

        response = self.make_request("setProduct", payload, method="POST")
        return response
