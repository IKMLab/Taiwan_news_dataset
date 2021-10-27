import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201910250015.aspx'
    response = news.crawlers.util.request_url.get(url=url)

    raw_news = news.crawlers.db.schema.RawNews(
        company_id=company_id,
        raw_xml=news.crawlers.util.normalize.compress_raw_xml(
            raw_xml=response.text,
        ),
        url_pattern=news.crawlers.util.normalize.compress_url(
            company_id=company_id,
            url=url,
        )
    )

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            美國副總統彭斯美東時間24日中午在華府智庫威爾遜中心(Wilson Center)舉辦的首屆
            馬勒克公共服務領袖講座上致詞,以下是他的演說全文: 謝謝大家的熱烈歡迎。新任董事長
            華克前州長、前眾議員哈曼,具有歷史性的威爾遜中心的各位董事們,各位傑出的學者,
            我很榮幸來到威爾遜中心。本中心的命名是為了紀念威爾遜總統,他是個偉人,在全球舞台上
            提倡美國的領導地位與自由。 今天上午,讓我以跟那一樣的精神,代另一位總統問候大家,
            他在國內與海外提倡自由,也就是美國第45任總統川普。 今天是一個重要的星期的結尾,
            土耳其剛入侵敘利亞。由於美國總統強有力的外交與經濟作為,同時因為我們與土耳其與
            庫德盟友的合作,敘利亞部隊能夠從邊界安全撤退,改由土耳其軍方控制。昨天,土耳其國防部
            證實永久停火,並停止一切攻擊性軍事行動。我們的部隊將要回國。 我很高興跟大家報告,
            透過這次停火,土耳其與我們的庫德族盟友創造了一個機會,讓國際社會可以成立一個安全
            地帶,我們相信可以為這個戰亂的地區重新帶來和平與安全。這確實是個進步。 因此,再次
            感謝讓我有這個榮幸來到這裡。能在此發表第一場佛烈德‧馬勒克紀念演講,是個特別的
            榮譽。認識佛烈德的人都知道,他是西點軍校傑出的畢業生,畢生服膺西點責任、榮譽、
            國家的校訓。他在給別人建議時,他經常引述西點學生的祈禱文,鼓勵他們「選擇較困難的
            正確道路,而非較輕鬆的錯誤道路」。 他瞭解沒有一個人,更不用說國家,能夠藉著放棄價值
            來捍衛自身的權益。因此,為了紀念他,我今天在此要討論一個攸關21世紀命運的重要議題:
            美國與中國的關係。 本屆政府任期剛開始,川普總統就決心在坦誠、公平與相互尊重的
            基礎上建立與中國的關係,這是為了創造一個「更公平、更安全、更和平的世界」。
            去年10月,我講到中國對美國利益與價值造成很大傷害的諸多政策,從中國的債務外交、
            軍事擴張主義、對教徒的壓迫、打造監控全民的國度,到中國各項不利自由公平貿易的政策,
            包括關稅、配額、操縱貨幣、強迫技術轉移與產業補貼。 美國行政部門持續更迭,每任政府
            都知道有這些問題,但過去沒有一個政府願意打破華府建立已久的利益,不僅容許這些問題,
            甚至從中獲利。面對中國經濟侵略與侵犯人權的行為,美國政壇不僅保持緘默,而且往往助長
            這些問題。隨著一年一年過去,美國內陸一家一家工廠關閉,隨著北京一棟一棟摩天大樓興建
            起來,美國工人愈來愈感到氣餒,中國則是膽子愈來愈大。 在不到20年間,就像川普總統
            所言,我們見到世界史上規模最大的財富轉移。在過去17年,中國的國內
            生產毛額成長了9倍以上,成為全球第二大經濟體。這個成長有很大部分是靠著美國在
            中國的投資所帶動。北京的行動造成美國對中國貿易赤字在去年達到4000億美元,
            幾乎占美國對全球貿易赤字的一半。川普總統曾多次表示,我們在過去25年重建了中國。
            此話真是一針見血!但以後不會再這樣了。 歷史肯定將會記載,在不到3年之內,川普總統
            永遠改變了這樣的情勢。美國與它的領導人不會再單單指望經濟往來,能讓中國的共黨
            獨裁政權國家轉化成為自由開放的社會,會尊重私人財產與法治以及國際商業規範。
            川普總統的2017年國家戰略報告載明,美國如今體認,中國是個經濟與戰略對手。
            我可以提供第一手的證明,美國都市與農村的大多數民眾支持川普總統對美中關係的真知灼見。
            川普總統的立場也獲得國會兩黨的廣泛支持。在過去一年,藉著那樣的支持,川普總統採取
            了大膽果斷的行動,改正過去失敗的政策,增強美國實力,要北京負起責任,使雙邊關係
            走在更公平、更穩定且具有建設性的道路之上,以符合兩國與全球的利益。 川普政府就任時,
            中國原本將成為全球最大經濟體。專家預測,中國的經濟規模將在短短幾年之內超越美國。
            但由於川普總統推動大膽的經濟政策,一切已經改觀。在本屆政府上任初期,川普總統就
            批准美國史上最大的減稅行動,我們降低了美國的企業稅率,跟其他國家的企業稅率相匹配,
            我們減少聯邦政府法規到史上最低限度,釋放了美國的能量;川普總統力挺自由公平的
            貿易。 結果是,美國創造了世界史上最強大的經濟。這也是美國在國內史上經濟最強的時候。
            目前的失業率是50年來最低,就業人口創下新高。家庭收入中位數在過去兩年半
            成長了5000美元以上,這還不包括川普總統減稅與能源改革為工作家庭所帶來的節省開銷
            效益。因為有了川普總統的政策,美國民眾的財富增加了數兆美元之多,中國的經濟則持續
            落在美國之後。 為了給美國工人打造公平的競爭環境,因應不道德的工作條件,川普總統
            在去年宣布對價值2500億美元的中國商品課徵關稅。今年稍早,總統宣布,如果美中貿易的
            重要問題在今年12月仍未獲得解決,將對另外價值3000億美元的中國商品課稅。 為了保障
            智慧財產權與我國民眾的隱私權及國家安全,我們採取強有力的措施以抑制華為、中興
            等中國企業的非法行為。我們並且敦促在全球的盟友建立安全的5G網路,不讓北京控制我們
            敏感的基礎設施與資料。 隨著我們經濟的成長,川普總統簽署一個世代以來最大幅度的
            軍費成長,過去3年,政府就在國防方面做了2.5兆美元的新投資,使得全球史上最強大的
            三軍更為強大。 為了讓北京瞭解沒有一個國家可以宣稱公海為領海,美國在過去一年增加
            了自由航行行動的步調與規模,增強我們在印太地區的軍事能見度。為了捍衛各地愛好自由
            的人民的價值,我們也點名中國迫害人民的宗教自由。中國有數以百萬計的少數民族與弱勢
            宗教信徒,面對當局消滅他們宗教與文化認同的企圖,中國共產黨逮捕基督教牧師、禁止販售
            聖經、拆毀教堂,並且監禁100多萬的維吾爾族穆斯林。 我們要求中國為迫害新疆的
            穆斯林少數民族負責,上個月,川普總統對中共官員採取簽證限制,並且制裁20個公安單位
            與8家中國企業,因為它們涉及對維吾爾人與中國其他穆斯林的壓迫。 我們跟台灣站在一起,
            捍衛台灣得來不易的自由,川普政府授權更多的對台軍售,並認同台灣是世界主要貿易經濟體,
            更是中華文化和民主的燈塔。 隨著數百萬人走上街頭,進行和平示威,我們代表香港人發聲,
            川普總統從一開始就說得很明白,必須用和平解決方案來尊重香港民眾的權益,一如1984英中
            聯合聲明所闡述。這些都是歷史性行動。過去沒有一位總統如此強烈的在美中關係之中推動
            美國利益。 針對美國的行動和決心,部分跨國企業說我們的經濟政策過於強硬,促進美國利益
            和價值觀不利於美國與中國建立更好的雙邊關係。當然,我們看法非常不同。 即便強權
            競爭如火如荼進行著,即便美國實力日益增強,美國仍希望中國更好。 因此,數十年來頭一遭,
            在總統川普領導下,美國對待中國領袖的方式,和其他任何一個偉大國家領袖的方式如出一轍,
            也就是尊重、一貫和坦誠。 本著坦誠的精神,我必須告訴諸位,從我自哈德遜研究所演說
            至今一年來,北京仍未採取重大措施來改善美中經濟關係。 還有在我們提出的其他問題方面,
            北京的舉止愈來愈具侵略性,也愈來愈不利於穩定。今年5月,在貿易問題上,多月辛苦磋商
            讓許多關鍵議題取得成果,中國卻在最後一刻打退堂鼓,撤回150頁的協議,讓雙方一切歸零
            重新來過。 川普總統依舊相信北京希望達成協議。我們樂見美國農民對最新第一階段協議
            的支持,希望能在智利舉行的亞太經濟合作組織(APEC)峰會順利簽署。 但中國明白,兩國
            之間仍有廣泛議題有結構性和明顯歧異有待解決,例如,即便中國領袖2015年在白宮玫瑰花園
            承諾,會停止相關作為,但中國依舊協助與唆使竊取美國智慧財產的行動。 今年7月,美國
            聯邦調查局局長告訴國會,FBI積極偵辦的1000起智財竊盜案件當中,多數與中國有關。
            美國企業每年蒙受數千億美元的智財權損失。這些數據背後牽扯的不僅僅只是業務,而是個人
            和家庭。 他們的權利被侵犯,天賦被竊取,夢想也跟著岌岌可危。自由企業仰賴民眾
            放手一搏追求抱負,只求一切的犧牲終有一天能有所收穫。當心血遭竊、汗水成泡影,
            這也重挫了我們整個自由企業制度。 去年發生一件又一件與中國有關的智財權竊盜案,
            特斯拉3月對一名前工程師提告。這名工程師在竊取30萬份公司檔案、竊走美國研發的
            自動駕駛技術後,跳槽到中國自駕車公司任職。 去年12月,美國司法部宣布偵破一惡名昭彰
            駭客團體進行了將近4年駭客行動,而這群駭客就在中國國家安全部工作。這些中國官員
            除竊走10萬筆海軍人員的姓名和個資,也竊取船艦維修資訊,嚴重威脅美國國家安全。 儘管
            中國承諾打擊中國芬太尼、鴉片類藥物,事實是,這些致命藥物同樣持續湧進美國邊境,每個月
            奪走數千名美國人的性命。 今天,中國共產黨在打造一個全球前所未見的監督政府,在至高點
            架設數億個監視錄影器。少數族裔必須在檢查哨依警方要求留下血液檢體、指紋、聲音紀錄、
            不同角度的大頭照,甚至虹膜掃描。 中國甚至把這些用在它獨裁政權的科技工具,出口
            給非洲、拉丁美洲、中東等地的國家。這些工具部署在諸如新疆這樣的地方,這些工具經常
            是在美國企業協助下部署完成。 北京也打破民間和軍方科技領域的界線,中國官方將此政策
            稱為「軍民融合」。依法律規定或國家主席下令,在中國的企業,無論是國營、民營還是外資,
            都必須跟中國軍方分享科技。 中國過去一年無論是區域間的軍事行動還是與鄰國互動,
            都日益挑釁,中國領袖2015年在白宮玫瑰花園承諾說,他們無意將南海軍事化,後來
            卻在人工島礁建築軍事設施並部署先進的反艦和防空飛彈系統。 北京同時加強運用他們所謂
            的海警船艦,例行性恐嚇菲律賓和馬來西亞的水手和漁民。中國海警甚至在越南外海以強力
            手段對待鑽探石油和天然氣的越南人。 2019年在東海,美國親近盟友日本為因應中國的
            挑釁,出動戰鬥機攔截的次數已一步步走向歷史新高。中國武警一連60天派遣船隻至日本管轄
            的尖閣諸島(釣魚台)周邊海域。 中國同時利用一帶一路倡議在全球各地港口站穩腳跟,
            雖說大多是為了商業目的,但這些商業目的最終都可能轉為軍事目的。 今天,中國國旗飄揚
            在斯里蘭卡、巴基斯坦、希臘等地的港口。今年稍早,據傳北京簽署秘密協議,要在柬埔寨
            打造海軍基地。也有傳聞說,北京甚至覬覦幾個大西洋地點,要當成海軍基地。 儘管川普政府
            將持續遵守一中政策,遵守中美三個聯合公報和台灣關係法,但中國透過金錢外交,在過去一年
            再誘使兩國與台斷交,改與中國建交,藉此對台灣民主施壓。國際社會永遠不該忘記,它與台灣
            的交往不會威脅到和平,而是會保衛台灣及整個區域的和平。 美國將始終相信,台灣擁抱
            民主,為全體華人展現出一條較好的道路。 過去一年,最能展現中共對自由強烈反感的事件,
            莫過於香港的示威。香港做為中國與廣大世界接觸的門戶,已經長達150年。香港是全球
            最自由的經濟體之一,有堅強而獨立的法律機構、活躍而自由的媒體,也有數十萬名外籍人士
            居住在此。從香港可以看到如果中國擁抱自由,可以有什麼成果,但過去幾年,北京加強對
            香港的干預,從事限制香港人民權利與自由的行動。而這些權利與自由是國際協議所保障的,
            也就是一國兩制。 川普總統已清楚說明,如同他所言,美國支持自由,我們尊重國家的主權,
            但美國也期望中國能遵守承諾,川普總統清楚說過,如果當局最後用暴力對付香港示威者,
            我們與中國達成貿易協定會十分困難。 從那時起,我很欣慰觀察到香港當局已撤回引發抗爭
            的逃犯條例。北京也展現一些克制。放眼未來幾日,我向你保證,美國會持續敦促中國克制,
            遵守承諾並尊重香港民眾,對數百萬在過去幾個月和平示威保護你們權利的民眾,我們與你
            站在一起。我們受你們的啟發。我們敦促你們維持非暴力抗爭的路徑。我們知道有
            數以百萬計的美國人為你們祈禱,對你們心懷敬意。 當中國在區域間和世界發揮影響力時,
            如同我去年所說,中國共產黨持續利誘與脅迫美國企業、製片商、大學、智庫、學者、
            記者和各州與聯邦政府官員,影響美國的公眾論壇,今天中國不僅向美國外銷大筆金額的
            不公平貿易商品,近期還外銷檢查制度,這是他們政權的標誌。北京利用企業的貪婪,
            試圖影響公眾意見,脅迫美國企業。有太多美國跨國企業在中國金錢和市場的引誘之下磕頭,
            不僅限制對中共的批評,也限制肯定美國價值的發言。 耐吉自詡倡導社會正義,但到了香港,
            卻將社會正義擱在門外。耐吉在中國的分店下架休士頓火箭隊的商品,以響應中國政府對
            火箭隊總經理英文7字推文「為自由而戰,力挺香港」的批判。有些美國職籃知名球員
            和老闆經常行使批評美國的自由,但面對中國人民自由與權利的問題時,卻悶不作聲。
            美國職籃選擇站在中共的一邊,限制言論自由,像是所有權完全屬於那個極權政府的分公司。
            號稱進步企業文化卻惡意忽視侵犯人權的行為,那不叫進步,而是壓迫。 當美國企業、
            職業運動與職業運動員擁抱檢查制度,這不僅是個錯誤,而且不合美國的風格。美國企業
            應該要力挺美國價值,不論是在國內或在世界各地。北京的經濟和戰略行動,與形塑美國輿論
            的企圖,證明了我一年前所說的話,而且今天也還是一樣。中國想要有個不一樣的美國總統,
            而這是川普總統的領導發揮功效的最終證明。美國經濟每天都在進步,中國則在付出代價。
            川普總統的策略是正確的,他在為美國人奮鬥,為美國的就業與勞工奮鬥,勝於美國歷任總統。
            我向你保證,川普政府不會退縮。 話雖如此,川普總統表明,美國不想與中國對峙,而是追求
            公平的環境、開放市場、公平貿易以及尊重我們的價值。我們也不要圍堵中國的發展,我們
            希望與中國領導人有建設性關係,就如同幾個世代的美國人與中國人民的關係那樣。如果中國
            往前跨一步,把握這個特殊的歷史時刻,重新開始,停止長期占美國人便宜的經貿手段,我知道
            川普總統已準備好,也願意展開新的未來。 就如同美國過去所為,當鄧小平推動改革開放
            政策,鼓勵與外界互動交流,美國以張開雙臂歡迎回應,我們歡迎中國崛起,我們慶賀6億人
            脫貧的顯著成就,美國對中國經濟興起的投資超越世界各國。美國人民希望中國人民過得更好
            。但要達成那個目標,我們必須因應當前狀態下的中國,而非我們想像或希望未來有天可能
            出現的中國。 人們有時會問川普政府是不是要和中國分手,答案絕對是「不是」。美國尋求
            與中國往來,中國也希望投入世界,但要往來,必須始終保持公平、相互尊重與國際經貿規則,
            但至今中共似乎仍抗拒真正的開放,不願融入全球的規範。北京今日所為,從中共在網路空間
            建立的防火牆,在南海抽砂建立的海上長城,從不信任香港自治,或壓制人民信仰,在在顯示
            數十年來,是中共背離廣大的世界。 我聽說習主席在中國共產黨內崛起擔任總書記後的
            一段秘密談話,中國必須認真做好準備,在兩種社會制度的方方面面既合作又鬥爭。他當時
            也告訴同僚,不可低估西方的韌性。這些話有其智慧。中國絕對不能低估熱愛自由的美國
            人民的韌性,以及美國總統的決心。 中國應該知道美國價值的深度,對這些價值的承諾堅定
            一如建國的元首,在美國自由與民主的光明不會有消逝的一天。 美國是因為反抗壓迫與暴政
            而誕生。我國是由勇敢卓絕、堅定果敢、信心十足、堅守獨立與鋼鐵意志的先賢們所創立、
            安定與領導。兩個多世紀以來,並沒有太多的變化。美國相信人人生而平等,享有特定
            與生俱來的權利:生命權、自由權與追求幸福的權利。沒有任何事情能改變這個信念。
            他們就是我們,未來也永遠如此。我們將繼續相信,民主、個人自由、宗教與良心自由、法治
            的價值符合美國與全球的利益,因為它現在與未來都能構成最好的政府,可以釋放人們的希望,
            並且指引世界各國之間的關係。 儘管我們在美中關係上面對諸多挑戰,我可以跟各位保證,
            在川普總統領導下,美國不會允許這些挑戰阻礙與中國的務實合作。我們將持續秉持善意與
            中國進行談判,以達成彼此經貿關係早該達成的結構性改革。我今早再次聽到,川普總統對於
            達成協定依然樂觀。 我們繼續透過教育、旅行與文化交流加強兩國人民的聯繫。美國與中國
            將繼續秉持交往的精神,共同努力達成北韓在可驗證的前提下全面非核化。我們也將在武器
            管制與在波斯灣的制裁方面加強合作。 美國將繼續尋求與中國改善關係。在這個過程中,
            我們會有話直說,因為這是美國跟中國都必須搞好的關係。美國將繼續追求美中關係根本性
            的變革。在川普總統的領導下,美國不會動搖。美國人民與兩黨民選官員將保持堅定。
            我們將捍衛我們的利益,我們將捍衛我們的價值。在這過程中,我們將秉持對所有人保持慈善
            與善意的精神。 川普總統與習近平主席建立深厚的私人關係。在那個基礎上,我們將繼續
            設法改善關係,為兩國人民帶來益處。我們深信,美國與中國可以也必須共同打造和平與繁榮
            的未來,但那個未來唯有靠誠實的對話與善意的談判才能實現。 我以去年演說的結語,
            結束我今天的講話。美國在向中國張開雙臂,我們希望不久之後,北京也做同樣的事,但這次
            不要光是講話,而是有所行動,並且恢復對美國的尊重。 中國有句古諺說,人只能看到眼前,
            上天可以預見未來。在未來的時日,讓我們以決心和信心追求和平繁榮的未來。對川普總統的
            領導與對美國經濟與全球地位的願景有信心,對他與中國國家主席習近平建立的關係有信心,
            也對美國人民與中國人民長久的友誼有信心。同時相信上天能看見未來。 憑藉著上帝的
            恩典,美國與中國將共同迎接那個未來。謝謝,上帝保佑各位,上帝保佑美國。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1571932800
    assert parsed_news.reporter == '台北'
    assert parsed_news.title == '美國副總統彭斯再談中國政策 要北京別光說不練'
    assert parsed_news.url_pattern == '201910250015'
