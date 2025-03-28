import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

# https://rapidapi.com/Glavier/api/twitter135
load_dotenv()

HEADERS_RAPIDAPI = {
    "X-RapidAPI-Key": os.environ.get("X-RapidAPI-Key"),
    "X-RapidAPI-Host": "twitter135.p.rapidapi.com",
}

# https://jojapi.com/api/twitter
HEADERS_JoJAPI = {
    "X-JoJAPI-Key": os.environ.get("X-JoJAPI-Key"),
}

SLEEP_TIME = 2


class TwitterGlavierAPI:
    def __init__(self, supplier: str = "rapidapi"):
        self.supplier = supplier
        if supplier == "rapidapi":
            self.headers = HEADERS_RAPIDAPI
            self.url_append = "https://twitter135.p.rapidapi.com/"
        elif supplier == "jojapi":
            self.headers = HEADERS_JoJAPI
            self.url_append = "https://twitter.jojapi.net/"

    def get_followers(self, username: str, cursor: str) -> pd.DataFrame:
        followers = self.get_followers_light(username, cursor)
        return followers

    def get_followers_light(self, username: str, cursor: str) -> pd.DataFrame:
        url = self.url_append + "v1.1/Followers/"
        followers = self.get_request(username, cursor, url)
        return followers

    def get_following(self, username: str, cursor: str) -> pd.DataFrame:
        followers = self.get_following_light(username, cursor)
        return followers

    def get_following_light(self, username: str, cursor: str) -> pd.DataFrame:
        url = self.url_append + "v1.1/Following/"
        following = self.get_request(username, cursor, url)
        return following

    def get_request(self, username: str, cursor: str, url: str) -> dict:
        querystring = {"username": username, "count": "200"}
        if cursor is not None:
            querystring["cursor"] = cursor
        more_users = True
        users = []
        request_num = 0

        while more_users:
            time.sleep(SLEEP_TIME)
            print(f"Request number: {request_num}")
            response = requests.get(url, headers=self.headers, params=querystring)
            try:
                print(f"Response: {response.raise_for_status()}")
            except requests.HTTPError:
                print(f"Request failed. Retrying in {SLEEP_TIME}s...")
            else:
                print(f"Got {len(response.json()['users'])} users")
                users += response.json()["users"]
                more_users = response.json()["next_cursor_str"] != "0"
                if more_users:
                    print(f"Next cursor: {response.json()['next_cursor_str']}")
                    querystring["cursor"] = response.json()["next_cursor_str"]
                    request_num += 1

        rest_ids = [user["id_str"] for user in users]
        more_details = self.get_details_by_ids(rest_ids, True)

        print(f"Got {len(users)} users")
        df = pd.DataFrame.from_dict(users)
        df["is_blue_verified"] = more_details

        df = df[df.protected == False]

        df.drop(
            columns=[
                "id_str",
                "location",
                "entities",
                "protected",
                "fast_followers_count",
                "normal_followers_count",
                "listed_count",
                "created_at",
                "favourites_count",
                "utc_offset",
                "time_zone",
                "geo_enabled",
                "verified",
                "statuses_count",
                "media_count",
                "lang",
                "status",
                "contributors_enabled",
                "is_translator",
                "is_translation_enabled",
                "profile_background_color",
                "profile_background_image_url",
                "profile_background_image_url_https",
                "profile_background_tile",
                "profile_image_url",
                "profile_image_url_https",
                "profile_banner_url",
                "profile_link_color",
                "profile_sidebar_border_color",
                "profile_sidebar_fill_color",
                "profile_text_color",
                "profile_use_background_image",
                "has_extended_profile",
                "default_profile",
                "default_profile_image",
                "pinned_tweet_ids",
                "pinned_tweet_ids_str",
                "has_custom_timelines",
                "can_media_tag",
                "followed_by",
                "following",
                "live_following",
                "follow_request_sent",
                "notifications",
                "muting",
                "blocking",
                "blocked_by",
                "advertiser_account_type",
                "advertiser_account_service_levels",
                "business_profile_state",
                "translator_type",
                "withheld_in_countries",
                "require_some_consent",
            ],
            inplace=True,
        )
        return df

    def get_user_by_screenname(self, username: str) -> str:
        url = self.url_append + "v2/UserByScreenName/"
        querystring = {"username": username}
        response = requests.get(url, headers=self.headers, params=querystring)
        try:
            print(f"Response: {response.raise_for_status()}")
        except requests.HTTPError:
            print(f"Request failed. Retrying in {SLEEP_TIME}s...")
            time.sleep(SLEEP_TIME)
        else:
            userid = response.json()["data"]["user"]["result"]["rest_id"]

        return userid

    def get_details_by_ids(self, ids: list, verified_status: bool = False) -> list:
        url = self.url_append + "v2/UsersByRestIds/"
        size = 300
        user_details = []
        request_num = 0
        while request_num < int(len(ids) / size) + 1:
            time.sleep(SLEEP_TIME)
            print(f"Request number: {request_num}")
            querystring = {"ids": ",".join(ids[0 + size * request_num : size + size * request_num])}
            response = requests.get(url, headers=self.headers, params=querystring)
            try:
                print(f"Response: {response.raise_for_status()}")
            except requests.HTTPError:
                print(f"Request failed. Retrying in {SLEEP_TIME}s...")
            else:

                for result in response.json()["data"]["users"]:
                    if verified_status:
                        try:
                            user_details.append(result["result"]["is_blue_verified"])
                        except KeyError:
                            print(f"KeyError: {result}")
                            user_details.append("False")
                    else:
                        user = {"is_blue_verified": ["is_blue_verified"]}
                        user.update(result["result"]["legacy"])
                request_num += 1

        return user_details


def main():
    twitter_api = TwitterGlavierAPI()
    ids = [
        "917177671691378688",
        "1052332852157849600",
        "1021860329926479872",
        "1213202268717080576",
        "22692523",
        "1005101715341770752",
        "14300230",
        "796687290089295872",
        "1175130632323833858",
        "1230861398055563264",
        "123276343",
        "22637974",
        "1047924493921005569",
        "1302042732714692609",
        "1635004022506627073",
        "71795203",
        "1654409519794098182",
        "1605807380943450112",
        "1787857874535751680",
        "1421253326360829954",
        "1540368495220760582",
        "1306359926164516864",
        "136447948",
        "1755387977885216768",
        "828788113451339776",
        "1755765196755247104",
        "708208770",
        "1370163747973632003",
        "1561384217900187653",
        "1524350935967072256",
        "1703381250206007296",
        "1651306109385179150",
        "1689077014899171328",
        "1741525738933911552",
        "977294048",
        "1354600043223908362",
        "264817491",
        "1621895309566558208",
        "224388083",
        "1340333600668069888",
        "1062794719380463617",
        "215271518",
        "1545482241740095490",
        "1255649265717841926",
        "1733564032014073857",
        "1666193312",
        "1468103131737247748",
        "930269644686024709",
        "1196915259010768897",
        "1498271952884183041",
        "1287811809748099079",
        "1369873159466450950",
        "1480369168927047680",
        "1249140391",
        "1265037073",
        "605700792",
        "1162370120557223936",
        "35368840",
        "549767622",
        "1367272388",
        "1692531558815805440",
        "3553198514",
        "115905737",
        "3793308794",
        "1677464784122396672",
        "1355160933295935488",
        "565686132",
        "965699949512900608",
        "1075142947270742016",
        "912760227380023296",
        "877398425163096065",
        "62603893",
        "1524836434053582853",
        "1533911174",
        "3316376038",
        "1746536197999009792",
        "68511037",
        "1257845875717607424",
        "715550870323134465",
        "1469603575",
        "1353552768468987904",
        "16461706",
        "25869185",
        "1395192591868731392",
        "1448515199489634306",
        "76766018",
        "1344479261877559297",
        "98433780",
        "1366565625401909249",
        "2538322138",
        "1310683973622927369",
        "15226303",
        "1121608779332767744",
        "17881764",
        "20736511",
        "329495443",
        "1694139510051700736",
        "1685398521300631553",
        "823766058909761536",
        "861985805883109377",
        "1380555947542773760",
        "1372681304668569606",
        "1681056250463698945",
        "784078608105177088",
        "16228398",
        "1489056427842940935",
        "825521308515581952",
        "755071644",
        "1514274062255607812",
        "1261836135984234499",
        "131948686",
        "16573941",
        "67418441",
        "1679630389734678528",
        "10546442",
        "5402612",
        "26257166",
        "807095",
        "759251",
        "40927173",
        "1457338780738797572",
        "19426551",
        "250414171",
        "6446742",
        "18479513",
        "19923144",
        "965758544548114438",
        "1486473049146904576",
        "1579455680884391938",
        "970994516357472257",
        "890061634181373952",
        "193531602",
        "1404217022137970691",
        "226428094",
        "361289499",
        "2455740283",
        "1630283681284669445",
        "319495411",
        "1451410581051691015",
        "1520137928118259715",
        "43775786",
        "1628254517698473985",
        "1262192006123708416",
        "1368413271452160000",
        "1432172996739883008",
        "16825716",
        "783137960812163072",
        "1500204023240175618",
        "2557521",
        "1027325969298862081",
        "395416760",
        "107145555",
        "1744389318943109120",
        "1355194613854851074",
        "1632098656685027328",
        "3302525341",
        "1461338556",
        "258512916",
        "1506781045613633544",
        "1598508389033803776",
        "1681458028489441281",
        "1194632206028824576",
        "1461144645812080643",
        "158946720",
        "1660025377886969859",
        "1732446388422668288",
        "19677487",
        "1746624992463187968",
        "1218201923947548672",
        "1068707070935916545",
        "2324706140",
        "745866842",
        "1536443139539488770",
        "1196304745603817472",
        "1333049564736221184",
        "948224645018324992",
        "1025070736627716096",
        "735696970157674496",
        "1341427362538291201",
        "166304658",
        "1666244171768942597",
        "1410389119662952451",
        "478077645",
        "1320586178467401728",
        "1636907641107537920",
        "3520188396",
        "2496792366",
        "1656733937949868040",
        "1659630023203012654",
        "1633816245442076673",
        "1003976419817353216",
        "1616941614169030656",
        "405320861",
        "287273291",
        "991793898010890241",
        "1251578631937089536",
        "1458869705473761280",
        "581754424",
        "1609523695428444160",
        "1626629829364957184",
        "1557675847410147330",
        "112339185",
        "1335767902067286019",
        "733866952045694977",
        "2174720072",
        "30286178",
        "1541923961474146304",
        "1412462411630755841",
        "447661258",
        "1634269429147271169",
        "3433485560",
        "1639355213743022096",
        "1417686048579018753",
        "1429925231943045120",
        "1575902388258586628",
        "1242657456",
        "887724883",
        "204155850",
        "1226337351544135680",
        "1455686701632815109",
        "331382754",
        "2455407479",
        "4204551",
        "1591819965568532480",
        "54246225",
        "956037321035603971",
        "1422613101636210695",
        "158049457",
        "1362724558353104897",
        "766323368635330562",
        "1338904981068525569",
        "97914405",
        "132589870",
        "1212855300304199680",
        "1599941958516019201",
        "1384980327190339589",
        "881269556",
        "1544699466170523648",
        "1675219818335834112",
        "1636083218880385031",
        "14701577",
        "1298722863000649728",
        "1213896587576897537",
        "1512439325128105990",
        "248886124",
        "881486490",
        "1244652762039795714",
        "2452070935",
        "964322377814429696",
        "245200688",
        "1422806507800956929",
        "1704115660500942848",
        "714342707775148033",
        "984043960162226176",
        "899512732331855872",
        "33518610",
        "1461688946006499333",
        "1359278538696757249",
        "1363011694952394752",
        "4735244833",
        "1170450097722855427",
        "1458534045726482443",
        "842650290",
        "4685749051",
        "1689825113665855488",
        "188369814",
        "1529950070036119552",
        "38785623",
        "2544501210",
        "1560033899488722944",
        "1267273775386710022",
        "1319287761048723458",
        "12044602",
        "20445899",
        "1465324254774235138",
        "342811359",
        "871812758148452352",
        "287735479",
        "1020058453",
        "14379660",
        "65694678",
        "1021070377357795328",
        "976884195632001027",
        "1115465940831891457",
        "1380237485914136584",
        "455937214",
        "952384819",
        "855300206086168576",
        "89043072",
        "932630991298007041",
        "60783724",
        "17351167",
        "855481986290524160",
        "18469669",
        "2360241314",
        "1027041315110842368",
        "29856819",
        "109813243",
        "1016500264919031809",
        "14313332",
        "753617640355012608",
        "8559342",
        "926956622617837568",
        "110933821",
        "297564170",
        "473501690",
        "1413027896",
        "2916305152",
        "778195914854989825",
        "1561557541",
        "456910776",
        "61558281",
        "1045384655749427201",
        "1412491297080983555",
        "35490565",
        "1281457267582177280",
        "924813411069911041",
        "1344759366671589376",
        "1049265018280263680",
        "1365386567355822080",
        "1446932149148344320",
        "1298770042381897729",
        "971046392872521730",
        "308811676",
        "3185716686",
        "1465216173612871681",
        "814964403284115457",
        "902926941413453824",
        "18856867",
        "1243933738951680003",
        "2561575478",
        "374670855",
        "284278132",
        "1101264495337365504",
        "1387497871751196672",
        "1202332588901195776",
        "61698439",
        "412833880",
        "195900371",
        "4918059373",
        "216173025",
        "9615462",
        "1436188011130200066",
        "1441468441983168513",
        "2453385626",
        "295218901",
        "1110877798820777986",
        "954831464939622400",
        "244647486",
        "1318028333041504256",
        "1202030125195374598",
        "1412281715347894274",
        "982364348038303744",
        "17849944",
        "22716009",
        "23847960",
        "56562803",
        "889220685423357956",
        "933113177197264896",
        "19454060",
        "349249475",
        "332617373",
        "44196397",
        "1349149096909668363",
    ]
    print(len(ids))
    users_details = twitter_api.get_details_by_ids(ids)
    print(users_details)
    print(len(users_details))


if __name__ == "__main__":
    main()
