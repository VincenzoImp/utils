import re
import numpy as np
from tqdm import tqdm
tqdm.pandas()

tlds = [".chirurgiens-dentistes.fr", ".andria-barletta-trani.it", ".andria-trani-barletta.it", ".barletta-trani-andria.it", ".friuli-venezia-giulia.it", ".monza-e-della-brianza.it", ".trani-andria-barletta.it", ".trani-barletta-andria.it", ".friuli-veneziagiulia.it", ".friulivenezia-giulia.it", ".barking-dagenham.sch.uk", ".bracknell-forest.sch.uk", ".andriabarlettatrani.it", ".andriatranibarletta.it", ".barlettatraniandria.it", ".friuliveneziagiulia.it", ".traniandriabarletta.it", ".tranibarlettaandria.it", ".trentino-alto-adige.it", ".trentino-sued-tirol.it", ".experts-comptables.fr", ".monzaedellabrianza.it", ".trentino-altoadige.it", ".trentino-sud-tirol.it", ".trentino-suedtirol.it", ".trentinoalto-adige.it", ".trentinosued-tirol.it", ".carbonia-iglesias.it", ".iglesias-carbonia.it", ".trentino-sudtirol.it", ".trentinoaltoadige.it", ".trentinosud-tirol.it", ".trentinosuedtirol.it", ".carboniaiglesias.it", ".friuli-ve-giulia.it", ".iglesiascarbonia.it", ".trentino-a-adige.it", ".trentino-s-tirol.it", ".trentinosudtirol.it", ".north-kazakhstan.su", ".geometre-expert.fr", ".campidano-medio.it", ".friuli-v-giulia.it", ".friuli-vegiulia.it", ".friulive-giulia.it", ".medio-campidano.it", ".reggio-calabria.it", ".trentino-aadige.it", ".trentino-stirol.it", ".trentinoa-adige.it", ".trentinos-tirol.it", ".kazimierz-dolny.pl", ".east-kazakhstan.su", ".travelersinsurance", ".ivano-frankivsk.ua", ".bournemouth.sch.uk", ".campidanomedio.it", ".dell-ogliastra.it", ".emilia-romagna.it", ".friuli-vgiulia.it", ".friuliv-giulia.it", ".friulivegiulia.it", ".mediocampidano.it", ".reggiocalabria.it", ".trentinoaadige.it", ".dnepropetrovsk.ua", ".dnipropetrovsk.ua", ".verm\u00f6gensberatung", ".ascoli-piceno.it", ".caltanissetta.it", ".carrara-massa.it", ".dellogliastra.it", ".emiliaromagna.it", ".friulivgiulia.it", ".massa-carrara.it", ".monza-brianza.it", ".monzaebrianza.it", ".pesaro-urbino.it", ".reggio-emilia.it", ".urbino-pesaro.it", ".valle-d-aosta.it", ".vibo-valentia.it", ".nieruchomosci.pl", ".blackburn.sch.uk", ".blackpool.sch.uk", ".doncaster.sch.uk", ".verm\u00f6gensberater", ".\u0ba8\u0bbf\u0bb1\u0bc1\u0bb5\u0ba9\u0bae\u0bcd.\u0b87\u0ba8\u0bcd\u0ba4\u0bbf\u0baf\u0bbe", ".americanexpress", ".ascolipiceno.it", ".carraramassa.it", ".cesena-forli.it", ".forli-cesena.it", ".massacarrara.it", ".monzabrianza.it", ".olbia-tempio.it", ".pesarourbino.it", ".reggioemilia.it", ".tempio-olbia.it", ".urbinopesaro.it", ".valle-daosta.it", ".valled-aosta.it", ".vibovalentia.it", ".kerryproperties", ".jelenia-gora.pl", ".stalowa-wola.pl", ".starachowice.pl", ".sandvikcoromant", ".khmelnitskiy.ua", ".barnsley.sch.uk", ".bradford.sch.uk", ".americanfamily", ".veterinaire.fr", ".alessandria.it", ".cesenaforli.it", ".forlicesena.it", ".olbiatempio.it", ".tempioolbia.it", ".val-d-aosta.it", ".valledaosta.it", ".kerrylogistics", ".boleslawiec.pl", ".swinoujscie.pl", ".vladikavkaz.ru", ".arkhangelsk.su", ".tselinograd.su", ".vladikavkaz.su", ".zaporizhzhe.ua", ".bathnes.sch.uk", ".weatherchannel", ".parliament.cy", ".pharmacien.fr", ".international", ".alto-adige.it", ".basilicata.it", ".campobasso.it", ".val-daosta.it", ".vald-aosta.it", ".lifeinsurance", ".fylkesbibl.no", ".babia-gora.pl", ".bialowieza.pl", ".bieszczady.pl", ".kobierzyce.pl", ".konskowola.pl", ".malopolska.pl", ".ostrowwlkp.pl", ".prochowice.pl", ".realestate.pl", ".swiebodzin.pl", ".tarnobrzeg.pl", ".pyatigorsk.ru", ".aktyubinsk.su", ".azerbaijan.su", ".mangyshlak.su", ".chernivtsi.ua", ".chernovtsy.ua", ".kirovograd.ua", ".sebastopol.ua", ".barnet.sch.uk", ".bexley.sch.uk", ".bolton.sch.uk", ".wolterskluwer", ".\u0995\u09cb\u09ae\u09cd\u09aa\u09be\u09a8\u09bf.\u09ad\u09be\u09b0\u09a4", ".charter.aero", ".aparecida.br", ".construction", ".chambagri.fr", ".agrigento.it", ".altoadige.it", ".benevento.it", ".catanzaro.it", ".frosinone.it", ".la-spezia.it", ".lombardia.it", ".ogliastra.it", ".pordenone.it", ".suedtirol.it", ".valdaosta.it", ".lplfinancial", ".folkebibl.no", ".bialystok.pl", ".bydgoszcz.pl", ".dlugoleka.pl", ".kolobrzeg.pl", ".ostroleka.pl", ".ostrowiec.pl", ".polkowice.pl", ".pomorskie.pl", ".przeworsk.pl", ".sosnowiec.pl", ".turystyka.pl", ".walbrzych.pl", ".wloclawek.pl", ".wodzislaw.pl", ".zachpomor.pl", ".zgorzelec.pl", ".bashkiria.ru", ".scholarships", ".bashkiria.su", ".karaganda.su", ".khakassia.su", ".krasnodar.su", ".togliatti.su", ".cherkassy.ua", ".chernigov.ua", ".brent.sch.uk", ".versicherung", ".\u0c15\u0c02\u0c2a\u0c46\u0c28\u0c40.\u0c2d\u0c3e\u0c30\u0c24\u0c4d", ".accountants", ".barclaycard", ".blackfriday", ".blockbuster", ".boavista.br", ".campinas.br", ".curitiba.br", ".salvador.br", ".bridgestone", ".calvinklein", ".pty-ltd.com", ".contractors", ".creditunion", ".engineering", ".enterprises", ".aeroport.fr", ".notaires.fr", ".ingatlan.hu", ".konyvelo.hu", ".ahmdabad.in", ".business.in", ".internet.in", ".investments", ".avellino.it", ".brindisi.it", ".cagliari.it", ".calabria.it", ".campania.it", ".florence.it", ".grosseto.it", ".laspezia.it", ".lombardy.it", ".macerata.it", ".oristano.it", ".piacenza.it", ".piedmont.it", ".piemonte.it", ".sardegna.it", ".sardinia.it", ".siracusa.it", ".trentino.it", ".verbania.it", ".vercelli.it", ".kerryhotels", ".lamborghini", ".motorcycles", ".olayangroup", ".photography", ".augustow.pl", ".jaworzno.pl", ".katowice.pl", ".limanowa.pl", ".mazowsze.pl", ".nowaruda.pl", ".podlasie.pl", ".pruszkow.pl", ".rawa-maz.pl", ".stargard.pl", ".swidnica.pl", ".szczecin.pl", ".szczytno.pl", ".warszawa.pl", ".playstation", ".productions", ".progressive", ".redumbrella", ".dagestan.ru", ".kalmykia.ru", ".kustanai.ru", ".mordovia.ru", ".vladimir.ru", ".abkhazia.su", ".ashgabad.su", ".balashov.su", ".chimkent.su", ".dagestan.su", ".kalmykia.su", ".kustanai.su", ".mordovia.su", ".murmansk.su", ".pokrovsk.su", ".tashkent.su", ".vladimir.su", ".cherkasy.ua", ".nikolaev.ua", ".ternopil.ua", ".uzhgorod.ua", ".zhitomir.ua", ".beds.sch.uk", ".bham.sch.uk", ".williamhill", ".\u0643\u0645\u067e\u0646\u06cc.\u0628\u06be\u0627\u0631\u062a", ".\u0b9a\u0bbf\u0b99\u0bcd\u0b95\u0baa\u0bcd\u0baa\u0bc2\u0bb0\u0bcd", ".accountant", ".cargo.aero", ".apartments", ".associates", ".basketball", ".bnpparibas", ".boehringer", ".floripa.br", ".capitalone", ".africa.com", ".consulting", ".creditcard", ".cuisinella", ".ekloges.cy", ".eurovision", ".extraspace", ".foundation", ".medecin.fr", ".healthcare", ".erotica.hu", ".erotika.hu", ".immobilien", ".gujarat.in", ".industries", ".abruzzo.it", ".belluno.it", ".bergamo.it", ".bologna.it", ".bolzano.it", ".brescia.it", ".caserta.it", ".catania.it", ".cosenza.it", ".cremona.it", ".crotone.it", ".ferrara.it", ".firenze.it", ".gorizia.it", ".imperia.it", ".isernia.it", ".laquila.it", ".liguria.it", ".livorno.it", ".lucania.it", ".mantova.it", ".messina.it", ".palermo.it", ".perugia.it", ".pescara.it", ".pistoia.it", ".potenza.it", ".ravenna.it", ".salerno.it", ".sassari.it", ".sicilia.it", ".sondrio.it", ".taranto.it", ".toscana.it", ".trapani.it", ".treviso.it", ".trieste.it", ".tuscany.it", ".venezia.it", ".vicenza.it", ".viterbo.it", ".management", ".mitsubishi", ".nextdirect", ".uenorge.no", ".beskidy.pl", ".bielawa.pl", ".cieszyn.pl", ".czeladz.pl", ".gniezno.pl", ".gorlice.pl", ".grajewo.pl", ".karpacz.pl", ".kartuzy.pl", ".kaszuby.pl", ".ketrzyn.pl", ".klodzko.pl", ".legnica.pl", ".lezajsk.pl", ".malbork.pl", ".mragowo.pl", ".olsztyn.pl", ".opoczno.pl", ".ostroda.pl", ".podhale.pl", ".pomorze.pl", ".rzeszow.pl", ".skoczow.pl", ".suwalki.pl", ".tourism.pl", ".wolomin.pl", ".wroclaw.pl", ".avocat.pro", ".pharma.pro", ".properties", ".protection", ".prudential", ".realestate", ".republican", ".restaurant", ".adygeya.ru", ".nalchik.ru", ".schaeffler", ".adygeya.su", ".armenia.su", ".bryansk.su", ".bukhara.su", ".georgia.su", ".ivanovo.su", ".karacol.su", ".karelia.su", ".nalchik.su", ".obninsk.su", ".troitsk.su", ".vologda.su", ".tatamotors", ".tourism.td", ".technology", ".agrinet.tn", ".defense.tn", ".tourism.tn", ".donetsk.ua", ".kharkiv.ua", ".kharkov.ua", ".kherson.ua", ".lugansk.ua", ".poltava.ua", ".vinnica.ua", ".university", ".vlaanderen", ".\u0915\u0902\u092a\u0928\u0940.\u092d\u093e\u0930\u0924", ".\u0a15\u0a70\u0a2a\u0a28\u0a40.\u0a2d\u0a3e\u0a30\u0a24", ".\u0a95\u0a82\u0aaa\u0aa8\u0ac0.\u0aad\u0abe\u0ab0\u0aa4", ".\u0e18\u0e38\u0e23\u0e01\u0e34\u0e08.\u0e44\u0e17\u0e22", ".accenture", ".allfinanz", ".amsterdam", ".analytics", ".aquarelle", ".barcelona", ".bloomberg", ".caxias.br", ".fortal.br", ".macapa.br", ".maceio.br", ".manaus.br", ".palmas.br", ".recife.br", ".christmas", ".community", ".directory", ".education", ".equipment", ".fairwinds", ".financial", ".firestone", ".avocat.fr", ".presse.fr", ".fresenius", ".furniture", ".goldpoint", ".hisamitsu", ".homedepot", ".homegoods", ".homesense", ".casino.hu", ".jogasz.hu", ".reklam.hu", ".tozsde.hu", ".utazas.hu", ".ltd.co.im", ".plc.co.im", ".travel.in", ".institute", ".insurance", ".ancona.it", ".aquila.it", ".arezzo.it", ".balsan.it", ".biella.it", ".chieti.it", ".foggia.it", ".genova.it", ".latina.it", ".marche.it", ".matera.it", ".milano.it", ".modena.it", ".molise.it", ".naples.it", ".napoli.it", ".novara.it", ".padova.it", ".puglia.it", ".ragusa.it", ".rimini.it", ".rovigo.it", ".savona.it", ".sicily.it", ".teramo.it", ".torino.it", ".trento.it", ".umbria.it", ".varese.it", ".veneto.it", ".venice.it", ".verona.it", ".kuokgroup", ".lancaster", ".landrover", ".lifestyle", ".marketing", ".marshalls", ".melbourne", ".microsoft", ".school.na", ".lg.gov.ng", ".idrett.no", ".museum.no", ".museum.np", ".travel.np", ".co.net.nz", ".health.nz", ".school.nz", ".museum.om", ".panasonic", ".bedzin.pl", ".elblag.pl", ".glogow.pl", ".kalisz.pl", ".lebork.pl", ".lowicz.pl", ".mazury.pl", ".miasta.pl", ".mielec.pl", ".mielno.pl", ".olecko.pl", ".olkusz.pl", ".powiat.pl", ".pulawy.pl", ".rybnik.pl", ".slupsk.pl", ".szkola.pl", ".travel.pl", ".warmia.pl", ".wegrow.pl", ".wielun.pl", ".pramerica", ".chiro.pro", ".nurse.pro", ".recht.pro", ".teach.pro", ".richardli", ".grozny.ru", ".marine.ru", ".shangrila", ".solutions", ".statebank", ".statefarm", ".stockholm", ".grozny.su", ".jambyl.su", ".kaluga.su", ".kurgan.su", ".termez.su", ".museum.tj", ".edunet.tn", ".travelers", ".crimea.ua", ".odessa.ua", ".vacations", ".health.vn", ".yodobashi", ".\u0645\u0648\u0631\u064a\u062a\u0627\u0646\u064a\u0627", ".abudhabi", ".airforce", ".allstate", ".north.am", ".radio.am", ".south.am", ".attorney", ".barclays", ".barefoot", ".bargains", ".baseball", ".boutique", ".belem.br", ".jampa.br", ".natal.br", ".radio.br", ".bradesco", ".broadway", ".brussels", ".builders", ".business", ".minsk.by", ".capetown", ".catering", ".catholic", ".cipriani", ".cleaning", ".clinique", ".clothing", ".commbank", ".computer", ".press.cy", ".delivery", ".deloitte", ".democrat", ".diamonds", ".discount", ".discover", ".download", ".engineer", ".ericsson", ".exchange", ".feedback", ".fidelity", ".firmdale", ".radio.fm", ".football", ".frontier", ".goodyear", ".grainger", ".graphics", ".hdfcbank", ".helsinki", ".holdings", ".hospital", ".adult.ht", ".perso.ht", ".agrar.hu", ".forum.hu", ".games.hu", ".hotel.hu", ".lakas.hu", ".media.hu", ".sport.hu", ".video.hu", ".bihar.in", ".delhi.in", ".infiniti", ".auz.info", ".ipiranga", ".istanbul", ".aosta.it", ".aoste.it", ".bozen.it", ".cuneo.it", ".fermo.it", ".genoa.it", ".lazio.it", ".lecce.it", ".lecco.it", ".lucca.it", ".milan.it", ".monza.it", ".nuoro.it", ".padua.it", ".parma.it", ".pavia.it", ".prato.it", ".rieti.it", ".siena.it", ".terni.it", ".turin.it", ".udine.it", ".akita.jp", ".kyoto.jp", ".osaka.jp", ".tokyo.jp", ".jpmorgan", ".phone.ki", ".seoul.kr", ".lighting", ".hotel.lk", ".lundbeck", ".press.ma", ".marriott", ".mckinsey", ".memorial", ".merckmsd", ".mortgage", ".perso.mr", ".perso.ne", ".other.nf", ".store.nf", ".maori.nz", ".observer", ".partners", ".pharmacy", ".pictures", ".bytom.pl", ".czest.pl", ".gmina.pl", ".ilawa.pl", ".jgora.pl", ".kepno.pl", ".konin.pl", ".kutno.pl", ".lomza.pl", ".lubin.pl", ".lukow.pl", ".media.pl", ".naklo.pl", ".olawa.pl", ".opole.pl", ".radom.pl", ".sanok.pl", ".sejny.pl", ".sklep.pl", ".slask.pl", ".targi.pl", ".tgory.pl", ".turek.pl", ".tychy.pl", ".ustka.pl", ".wlocl.pl", ".zagan.pl", ".zarow.pl", ".zgora.pl", ".plumbing", ".com.post", ".edu.post", ".org.post", ".acct.pro", ".dent.pro", ".prof.pro", ".property", ".redstone", ".reliance", ".store.ro", ".mytis.ru", ".saarland", ".samsclub", ".security", ".services", ".shopping", ".perso.sn", ".softbank", ".software", ".stcgroup", ".exnet.su", ".lenug.su", ".navoi.su", ".penza.su", ".sochi.su", ".supplies", ".perso.tn", ".training", ".hotel.tz", ".lutsk.ua", ".odesa.ua", ".rivne.ua", ".rovno.ua", ".volyn.ua", ".yalta.ua", ".vanguard", ".ventures", ".verisign", ".woodside", ".yokohama", ".\u0627\u0644\u0633\u0639\u0648\u062f\u064a\u0629", ".abogado", ".academy", ".agakhan", ".alibaba", ".android", ".athleta", ".info.au", ".auction", ".audible", ".auspost", ".info.az", ".name.az", ".banamex", ".bauhaus", ".bentley", ".bestbuy", ".name.bh", ".info.bi", ".auz.biz", ".booking", ".blog.br", ".coop.br", ".flog.br", ".taxi.br", ".vlog.br", ".wiki.br", ".brother", ".capital", ".caravan", ".careers", ".channel", ".charity", ".chintai", ".citadel", ".info.ck", ".clubmed", ".college", ".cologne", ".jpn.com", ".mex.com", ".company", ".compare", ".contact", ".cooking", ".corsica", ".country", ".coupons", ".courses", ".cricket", ".cruises", ".nome.cv", ".publ.cv", ".name.cy", ".dentist", ".digital", ".domains", ".info.ec", ".info.eg", ".name.eg", ".info.et", ".name.et", ".exposed", ".express", ".farmers", ".fashion", ".ferrari", ".ferrero", ".finance", ".fishing", ".fitness", ".info.fj", ".name.fj", ".flights", ".florist", ".flowers", ".forsale", ".asso.fr", ".gouv.fr", ".port.fr", ".frogans", ".fujitsu", ".gallery", ".genting", ".godaddy", ".mobi.gp", ".grocery", ".guitars", ".hamburg", ".hangout", ".hitachi", ".holiday", ".hosting", ".hotmail", ".asso.ht", ".firm.ht", ".info.ht", ".shop.ht", ".2000.hu", ".bolt.hu", ".city.hu", ".film.hu", ".info.hu", ".news.hu", ".priv.hu", ".shop.hu", ".suli.hu", ".szex.hu", ".hyundai", ".muni.il", ".coop.in", ".firm.in", ".info.in", ".post.in", ".ismaili", ".asti.it", ".bari.it", ".como.it", ".enna.it", ".lodi.it", ".pisa.it", ".roma.it", ".rome.it", ".jewelry", ".name.jo", ".saga.jp", ".juniper", ".info.ke", ".mobi.ke", ".info.ki", ".mobi.ki", ".kitchen", ".komatsu", ".lacaixa", ".lanxess", ".lasalle", ".latrobe", ".leclerc", ".limited", ".lincoln", ".assn.lk", ".conf.lv", ".markets", ".asso.mc", ".info.ml", ".monster", ".coop.mw", ".name.my", ".info.na", ".info.ne", ".auz.net", ".netbank", ".netflix", ".network", ".neustar", ".arts.nf", ".firm.nf", ".info.nf", ".mobi.ng", ".name.ng", ".info.ni", ".priv.no", ".aero.np", ".asia.np", ".coop.np", ".info.np", ".mobi.np", ".name.np", ".info.nr", ".geek.nz", ".kiwi.nz", ".okinawa", ".organic", ".origins", ".asso.pf", ".philips", ".pioneer", ".agro.pl", ".auto.pl", ".info.pl", ".lapy.pl", ".mail.pl", ".nysa.pl", ".pila.pl", ".pisz.pl", ".priv.pl", ".shop.pl", ".politie", ".info.pr", ".isla.pr", ".name.pr", ".aaa.pro", ".aca.pro", ".arc.pro", ".bar.pro", ".bus.pro", ".chi.pro", ".cpa.pro", ".den.pro", ".eng.pro", ".jur.pro", ".law.pro", ".med.pro", ".min.pro", ".nur.pro", ".prx.pro", ".rel.pro", ".vet.pro", ".coop.py", ".name.qa", ".realtor", ".recipes", ".rentals", ".reviews", ".rexroth", ".arts.ro", ".firm.ro", ".info.ro", ".samsung", ".sandvik", ".schmidt", ".schwarz", ".science", ".info.sd", ".shiksha", ".singles", ".univ.sn", ".staples", ".storage", ".tula.su", ".tuva.su", ".support", ".surgery", ".systems", ".temasek", ".theater", ".theatre", ".tickets", ".aero.tj", ".coop.tj", ".info.tj", ".name.tj", ".info.tn", ".intl.tn", ".rnrt.tn", ".toshiba", ".info.tr", ".name.tr", ".trading", ".info.tt", ".jobs.tt", ".mobi.tt", ".name.tt", ".club.tw", ".ebiz.tw", ".game.tw", ".info.tz", ".mobi.tz", ".kiev.ua", ".kyiv.ua", ".lviv.ua", ".sumy.ua", ".info.ve", ".info.vn", ".name.vn", ".walmart", ".wanggou", ".watches", ".weather", ".website", ".wedding", ".whoswho", ".windows", ".winners", ".yamaxun", ".youtube", ".zuerich", ".\u043a\u0430\u0442\u043e\u043b\u0438\u043a", ".\u0443\u043f\u0440.\u0441\u0440\u0431", ".\u0627\u0644\u0628\u062d\u0631\u064a\u0646", ".\u0627\u0644\u062c\u0632\u0627\u0626\u0631", ".\u0627\u0644\u0639\u0644\u064a\u0627\u0646", ".\u0643\u0627\u062b\u0648\u0644\u064a\u0643", ".\u067e\u0627\u0643\u0633\u062a\u0627\u0646", ".\u067e\u0627\u06a9\u0633\u062a\u0627\u0646", ".\u0b87\u0ba8\u0bcd\u0ba4\u0bbf\u0baf\u0bbe", ".abbott", ".abbvie", ".net.ae", ".org.ae", ".sch.ae", ".com.af", ".edu.af", ".gov.af", ".net.af", ".org.af", ".africa", ".com.ag", ".net.ag", ".nom.ag", ".org.ag", ".agency", ".com.ai", ".net.ai", ".off.ai", ".org.ai", ".airbus", ".airtel", ".com.al", ".edu.al", ".net.al", ".org.al", ".alipay", ".alsace", ".alstom", ".com.am", ".net.am", ".org.am", ".amazon", ".anquan", ".com.ar", ".int.ar", ".net.ar", ".org.ar", ".aramco", ".asn.au", ".com.au", ".net.au", ".org.au", ".author", ".com.aw", ".biz.az", ".com.az", ".edu.az", ".gov.az", ".int.az", ".mil.az", ".net.az", ".org.az", ".pro.az", ".com.ba", ".bayern", ".com.bb", ".net.bb", ".org.bb", ".com.bd", ".net.bd", ".org.bd", ".beauty", ".berlin", ".biz.bh", ".com.bh", ".edu.bh", ".net.bh", ".org.bh", ".bharti", ".com.bi", ".edu.bi", ".net.bi", ".org.bi", ".com.bj", ".com.bm", ".net.bm", ".org.bm", ".com.bn", ".net.bn", ".org.bn", ".com.bo", ".net.bo", ".org.bo", ".bostik", ".boston", ".abc.br", ".adm.br", ".adv.br", ".agr.br", ".app.br", ".arq.br", ".art.br", ".ato.br", ".bhz.br", ".bib.br", ".bio.br", ".bmd.br", ".bsb.br", ".cim.br", ".cng.br", ".cnt.br", ".com.br", ".des.br", ".det.br", ".dev.br", ".ecn.br", ".eco.br", ".edu.br", ".emp.br", ".enf.br", ".eng.br", ".esp.br", ".etc.br", ".eti.br", ".far.br", ".fnd.br", ".fot.br", ".foz.br", ".fst.br", ".g12.br", ".geo.br", ".ggf.br", ".gov.br", ".gru.br", ".imb.br", ".ind.br", ".inf.br", ".jor.br", ".lel.br", ".log.br", ".mat.br", ".med.br", ".mil.br", ".mus.br", ".net.br", ".nom.br", ".not.br", ".ntr.br", ".odo.br", ".org.br", ".poa.br", ".ppg.br", ".pro.br", ".psc.br", ".psi.br", ".qsl.br", ".rec.br", ".rep.br", ".rio.br", ".seg.br", ".sjc.br", ".slg.br", ".srv.br", ".tec.br", ".teo.br", ".tmp.br", ".trd.br", ".tur.br", ".vet.br", ".vix.br", ".zlg.br", ".broker", ".com.bs", ".net.bs", ".org.bs", ".com.bt", ".org.bt", ".net.bw", ".org.bw", ".com.by", ".net.by", ".com.bz", ".net.bz", ".org.bz", ".camera", ".career", ".casino", ".com.cd", ".net.cd", ".org.cd", ".center", ".chanel", ".chrome", ".church", ".com.ci", ".edu.ci", ".int.ci", ".net.ci", ".nom.ci", ".org.ci", ".circle", ".biz.ck", ".edu.ck", ".gen.ck", ".gov.ck", ".net.ck", ".org.ck", ".claims", ".clinic", ".com.cm", ".net.cm", ".com.cn", ".net.cn", ".org.cn", ".com.co", ".net.co", ".nom.co", ".coffee", ".ae.com", ".br.com", ".cn.com", ".co.com", ".de.com", ".eu.com", ".gr.com", ".hk.com", ".hu.com", ".it.com", ".kr.com", ".no.com", ".nv.com", ".qc.com", ".ru.com", ".sa.com", ".se.com", ".uk.com", ".us.com", ".za.com", ".comsec", ".condos", ".coupon", ".credit", ".cruise", ".com.cu", ".com.cv", ".edu.cv", ".int.cv", ".net.cv", ".org.cv", ".com.cw", ".net.cw", ".biz.cy", ".com.cy", ".ltd.cy", ".net.cy", ".org.cy", ".pro.cy", ".dating", ".datsun", ".com.de", ".dealer", ".degree", ".dental", ".design", ".direct", ".biz.dk", ".com.dm", ".net.dm", ".org.dm", ".art.do", ".com.do", ".net.do", ".org.do", ".sld.do", ".web.do", ".doctor", ".dunlop", ".dupont", ".durban", ".com.dz", ".com.ec", ".fin.ec", ".med.ec", ".net.ec", ".org.ec", ".pro.ec", ".com.ee", ".fie.ee", ".med.ee", ".pri.ee", ".com.eg", ".edu.eg", ".eun.eg", ".gov.eg", ".net.eg", ".org.eg", ".emerck", ".energy", ".com.es", ".edu.es", ".gob.es", ".nom.es", ".org.es", ".estate", ".biz.et", ".com.et", ".net.et", ".org.et", ".events", ".expert", ".family", ".biz.fj", ".com.fj", ".net.fj", ".org.fj", ".pro.fj", ".flickr", ".com.fr", ".nom.fr", ".prd.fr", ".futbol", ".gallup", ".garden", ".com.ge", ".edu.ge", ".gov.ge", ".mil.ge", ".net.ge", ".org.ge", ".pvt.ge", ".george", ".net.gg", ".org.gg", ".com.gh", ".edu.gh", ".org.gh", ".com.gi", ".gov.gi", ".ltd.gi", ".org.gi", ".giving", ".com.gl", ".edu.gl", ".net.gl", ".org.gl", ".global", ".com.gn", ".gov.gn", ".net.gn", ".org.gn", ".google", ".com.gp", ".net.gp", ".org.gp", ".com.gr", ".edu.gr", ".net.gr", ".org.gr", ".gratis", ".com.gt", ".ind.gt", ".net.gt", ".org.gt", ".com.gu", ".com.gy", ".net.gy", ".health", ".hermes", ".hiphop", ".com.hk", ".edu.hk", ".gov.hk", ".idv.hk", ".inc.hk", ".ltd.hk", ".net.hk", ".org.hk", ".com.hn", ".edu.hn", ".net.hn", ".org.hn", ".hockey", ".hotels", ".com.hr", ".art.ht", ".com.ht", ".edu.ht", ".net.ht", ".org.ht", ".pol.ht", ".pro.ht", ".rel.ht", ".org.hu", ".sex.hu", ".hughes", ".biz.id", ".web.id", ".net.il", ".org.il", ".com.im", ".net.im", ".org.im", ".imamat", ".biz.in", ".com.in", ".gen.in", ".ind.in", ".int.in", ".net.in", ".org.in", ".pro.in", ".insure", ".intuit", ".com.iq", ".abr.it", ".bas.it", ".cal.it", ".cam.it", ".emr.it", ".fvg.it", ".laz.it", ".lig.it", ".lom.it", ".mar.it", ".mol.it", ".pmn.it", ".pug.it", ".sar.it", ".sic.it", ".taa.it", ".tos.it", ".umb.it", ".vao.it", ".vda.it", ".ven.it", ".jaguar", ".net.je", ".org.je", ".com.jm", ".net.jm", ".org.jm", ".com.jo", ".net.jo", ".org.jo", ".sch.jo", ".joburg", ".juegos", ".kaufen", ".com.kg", ".net.kg", ".org.kg", ".com.kh", ".edu.kh", ".net.kh", ".org.kh", ".biz.ki", ".com.ki", ".edu.ki", ".gov.ki", ".net.ki", ".org.ki", ".tel.ki", ".kindle", ".com.km", ".nom.km", ".org.km", ".com.kn", ".edu.kn", ".gov.kn", ".kosher", ".com.kw", ".edu.kw", ".net.kw", ".org.kw", ".com.ky", ".net.ky", ".org.ky", ".com.kz", ".org.kz", ".latino", ".lawyer", ".com.lb", ".edu.lb", ".net.lb", ".org.lb", ".com.lc", ".net.lc", ".org.lc", ".lefrak", ".living", ".com.lk", ".edu.lk", ".grp.lk", ".ltd.lk", ".ngo.lk", ".org.lk", ".soc.lk", ".web.lk", ".locker", ".london", ".com.lr", ".org.lr", ".net.ls", ".org.ls", ".luxury", ".asn.lv", ".com.lv", ".edu.lv", ".mil.lv", ".net.lv", ".org.lv", ".com.ly", ".med.ly", ".net.ly", ".org.ly", ".plc.ly", ".sch.ly", ".net.ma", ".org.ma", ".madrid", ".maison", ".makeup", ".market", ".mattel", ".com.mg", ".mil.mg", ".net.mg", ".nom.mg", ".org.mg", ".prd.mg", ".com.mk", ".edu.mk", ".inf.mk", ".net.mk", ".org.mk", ".com.ml", ".net.ml", ".org.ml", ".biz.mm", ".com.mm", ".net.mm", ".org.mm", ".per.mm", ".com.mo", ".net.mo", ".org.mo", ".mobile", ".monash", ".mormon", ".moscow", ".edu.mr", ".org.mr", ".com.ms", ".org.ms", ".com.mt", ".edu.mt", ".net.mt", ".org.mt", ".com.mu", ".net.mu", ".nom.mu", ".org.mu", ".museum", ".com.mv", ".com.mw", ".edu.mw", ".int.mw", ".net.mw", ".org.mw", ".com.mx", ".net.mx", ".org.mx", ".com.my", ".edu.my", ".gov.my", ".mil.my", ".net.my", ".org.my", ".edu.mz", ".net.mz", ".org.mz", ".alt.na", ".com.na", ".edu.na", ".net.na", ".org.na", ".nagoya", ".com.ne", ".int.ne", ".org.ne", ".gb.net", ".hu.net", ".in.net", ".jp.net", ".ru.net", ".se.net", ".uk.net", ".com.nf", ".net.nf", ".org.nf", ".per.nf", ".rec.nf", ".web.nf", ".com.ng", ".edu.ng", ".gov.ng", ".net.ng", ".org.ng", ".sch.ng", ".biz.ni", ".com.ni", ".edu.ni", ".gob.ni", ".int.ni", ".mil.ni", ".net.ni", ".nom.ni", ".org.ni", ".web.ni", ".nissan", ".nissay", ".com.nl", ".net.nl", ".fhs.no", ".vgs.no", ".norton", ".nowruz", ".biz.np", ".com.np", ".mil.np", ".net.np", ".org.np", ".pro.np", ".biz.nr", ".com.nr", ".net.nr", ".org.nr", ".gen.nz", ".iwi.nz", ".net.nz", ".org.nz", ".office", ".olayan", ".biz.om", ".com.om", ".edu.om", ".gov.om", ".med.om", ".mil.om", ".net.om", ".org.om", ".pro.om", ".sch.om", ".online", ".oracle", ".orange", ".ae.org", ".hk.org", ".us.org", ".otsuka", ".abo.pa", ".com.pa", ".edu.pa", ".gob.pa", ".ing.pa", ".med.pa", ".net.pa", ".nom.pa", ".org.pa", ".sld.pa", ".com.pe", ".edu.pe", ".gob.pe", ".mil.pe", ".net.pe", ".nom.pe", ".org.pe", ".com.pf", ".edu.pf", ".gov.pf", ".org.pf", ".pfizer", ".com.pg", ".net.pg", ".org.pg", ".com.ph", ".net.ph", ".org.ph", ".photos", ".physio", ".pictet", ".biz.pk", ".com.pk", ".net.pk", ".org.pk", ".web.pk", ".aid.pl", ".atm.pl", ".biz.pl", ".com.pl", ".edu.pl", ".elk.pl", ".gsm.pl", ".mil.pl", ".net.pl", ".nom.pl", ".org.pl", ".rel.pl", ".sex.pl", ".sos.pl", ".waw.pl", ".net.pn", ".org.pn", ".biz.pr", ".com.pr", ".net.pr", ".org.pr", ".pro.pr", ".com.ps", ".net.ps", ".org.ps", ".com.pt", ".org.pt", ".com.py", ".edu.py", ".net.py", ".org.py", ".com.qa", ".edu.qa", ".mil.qa", ".net.qa", ".org.qa", ".sch.qa", ".quebec", ".racing", ".realty", ".reisen", ".repair", ".report", ".review", ".com.ro", ".nom.ro", ".org.ro", ".rec.ro", ".srl.ro", ".www.ro", ".rogers", ".edu.rs", ".org.rs", ".bir.ru", ".cbg.ru", ".com.ru", ".msk.ru", ".net.ru", ".nov.ru", ".org.ru", ".spb.ru", ".net.rw", ".org.rw", ".ryukyu", ".com.sa", ".edu.sa", ".med.sa", ".net.sa", ".org.sa", ".pub.sa", ".sch.sa", ".safety", ".sakura", ".sanofi", ".com.sb", ".net.sb", ".org.sb", ".com.sc", ".net.sc", ".org.sc", ".school", ".schule", ".com.sd", ".net.sd", ".com.se", ".search", ".secure", ".select", ".com.sg", ".edu.sg", ".net.sg", ".org.sg", ".shouji", ".org.sk", ".com.sl", ".edu.sl", ".net.sl", ".org.sl", ".art.sn", ".com.sn", ".edu.sn", ".org.sn", ".com.so", ".net.so", ".org.so", ".soccer", ".social", ".biz.ss", ".com.ss", ".net.ss", ".stream", ".studio", ".msk.su", ".nov.su", ".spb.su", ".supply", ".suzuki", ".com.sv", ".edu.sv", ".gob.sv", ".org.sv", ".swatch", ".com.sy", ".sydney", ".org.sz", ".taipei", ".taobao", ".target", ".tattoo", ".com.tc", ".net.tc", ".org.tc", ".pro.tc", ".com.td", ".net.td", ".org.td", ".tennis", ".tienda", ".biz.tj", ".com.tj", ".dyn.tj", ".int.tj", ".mil.tj", ".net.tj", ".org.tj", ".per.tj", ".pro.tj", ".web.tj", ".tjmaxx", ".tkmaxx", ".com.tl", ".net.tl", ".org.tl", ".com.tn", ".ens.tn", ".fin.tn", ".ind.tn", ".nat.tn", ".net.tn", ".org.tn", ".rns.tn", ".rnu.tn", ".toyota", ".bbs.tr", ".biz.tr", ".com.tr", ".gen.tr", ".net.tr", ".org.tr", ".tel.tr", ".web.tr", ".travel", ".biz.tt", ".com.tt", ".net.tt", ".org.tt", ".pro.tt", ".com.tw", ".idv.tw", ".mil.tw", ".net.tw", ".org.tw", ".mil.tz", ".biz.ua", ".com.ua", ".edu.ua", ".gov.ua", ".net.ua", ".org.ua", ".com.ug", ".org.ug", ".gov.uk", ".ltd.uk", ".net.uk", ".org.uk", ".plc.uk", ".sch.uk", ".unicom", ".com.uy", ".edu.uy", ".net.uy", ".org.uy", ".biz.uz", ".com.uz", ".net.uz", ".org.uz", ".com.vc", ".net.vc", ".org.vc", ".com.ve", ".net.ve", ".org.ve", ".web.ve", ".com.vi", ".net.vi", ".org.vi", ".viajes", ".viking", ".villas", ".virgin", ".vision", ".biz.vn", ".com.vn", ".edu.vn", ".gov.vn", ".int.vn", ".net.vn", ".org.vn", ".pro.vn", ".voting", ".voyage", ".com.vu", ".net.vu", ".org.vu", ".walter", ".webcam", ".com.ws", ".net.ws", ".org.ws", ".xihuan", ".yachts", ".yandex", ".com.ye", ".net.ye", ".org.ye", ".net.za", ".org.za", ".web.za", ".zappos", ".com.zm", ".org.zm", ".org.zw", ".\u043c\u043e\u0441\u043a\u0432\u0430", ".\u043e\u043d\u043b\u0430\u0439\u043d", ".\u043a\u043e\u043c.\u0440\u0444", ".\u043d\u0435\u0442.\u0440\u0444", ".\u043e\u0440\u0433.\u0440\u0444", ".\u0430\u043a.\u0441\u0440\u0431", ".\u043f\u0440.\u0441\u0440\u0431", ".\u0627\u0628\u0648\u0638\u0628\u064a", ".\u0627\u0631\u0627\u0645\u0643\u0648", ".\u0627\u0644\u0627\u0631\u062f\u0646", ".\u0627\u0644\u0645\u063a\u0631\u0628", ".\u0627\u0645\u0627\u0631\u0627\u062a", ".\u0641\u0644\u0633\u0637\u064a\u0646", ".\u0645\u0644\u064a\u0633\u064a\u0627", ".\u092d\u093e\u0930\u0924\u092e\u094d", ".\u0b87\u0bb2\u0b99\u0bcd\u0b95\u0bc8", ".\u30d5\u30a1\u30c3\u30b7\u30e7\u30f3", ".actor", ".adult", ".ac.ae", ".co.ae", ".aetna", ".co.ag", ".co.am", ".amfam", ".amica", ".co.ao", ".it.ao", ".apple", ".archi", ".co.at", ".or.at", ".id.au", ".audio", ".autos", ".co.az", ".pp.az", ".azure", ".co.ba", ".baidu", ".co.bb", ".ac.bd", ".beats", ".cc.bh", ".me.bh", ".co.bi", ".mo.bi", ".or.bi", ".bible", ".bingo", ".black", ".tv.bo", ".boats", ".bosch", ".am.br", ".fm.br", ".tv.br", ".build", ".ac.bw", ".co.bw", ".co.bz", ".za.bz", ".canon", ".cards", ".chase", ".cheap", ".ac.ci", ".co.ci", ".ed.ci", ".go.ci", ".in.ci", ".or.ci", ".cisco", ".citic", ".co.ck", ".click", ".cloud", ".co.cm", ".ac.cn", ".ah.cn", ".bj.cn", ".cq.cn", ".fj.cn", ".gd.cn", ".gs.cn", ".gx.cn", ".gz.cn", ".ha.cn", ".hb.cn", ".he.cn", ".hi.cn", ".hk.cn", ".hl.cn", ".hn.cn", ".jl.cn", ".js.cn", ".jx.cn", ".ln.cn", ".mo.cn", ".nm.cn", ".nx.cn", ".qh.cn", ".sc.cn", ".sd.cn", ".sh.cn", ".sn.cn", ".sx.cn", ".tj.cn", ".tw.cn", ".xj.cn", ".xz.cn", ".yn.cn", ".zj.cn", ".coach", ".codes", ".co.cr", ".ed.cr", ".fi.cr", ".go.cr", ".or.cr", ".sa.cr", ".crown", ".ac.cy", ".tm.cy", ".cymru", ".co.cz", ".dance", ".co.de", ".deals", ".delta", ".co.dk", ".co.dm", ".drive", ".dubai", ".earth", ".edeka", ".co.ee", ".tv.eg", ".email", ".epson", ".faith", ".fedex", ".final", ".ac.fj", ".co.fk", ".forex", ".forum", ".tm.fr", ".gallo", ".games", ".co.gg", ".gifts", ".gives", ".co.gl", ".glass", ".globo", ".gmail", ".green", ".gripe", ".group", ".gucci", ".guide", ".co.gy", ".\u516c\u53f8.hk", ".homes", ".honda", ".horse", ".house", ".co.hu", ".tm.hu", ".hyatt", ".co.id", ".my.id", ".or.id", ".ikano", ".ac.il", ".co.il", ".ac.im", ".co.im", ".5g.in", ".6g.in", ".ai.in", ".am.in", ".ca.in", ".cn.in", ".co.in", ".cs.in", ".dr.in", ".er.in", ".io.in", ".me.in", ".pg.in", ".tv.in", ".uk.in", ".up.in", ".us.in", ".co.ir", ".irish", ".ag.it", ".al.it", ".an.it", ".ao.it", ".ap.it", ".aq.it", ".ar.it", ".at.it", ".av.it", ".ba.it", ".bg.it", ".bi.it", ".bl.it", ".bn.it", ".bo.it", ".br.it", ".bs.it", ".bt.it", ".bz.it", ".ca.it", ".cb.it", ".ce.it", ".ch.it", ".ci.it", ".cl.it", ".cn.it", ".co.it", ".cr.it", ".cs.it", ".ct.it", ".cz.it", ".en.it", ".fc.it", ".fe.it", ".fg.it", ".fi.it", ".fm.it", ".fr.it", ".ge.it", ".go.it", ".gr.it", ".im.it", ".is.it", ".kr.it", ".lc.it", ".le.it", ".li.it", ".lo.it", ".lt.it", ".lu.it", ".mb.it", ".mc.it", ".me.it", ".mi.it", ".mn.it", ".mo.it", ".ms.it", ".mt.it", ".na.it", ".no.it", ".nu.it", ".og.it", ".or.it", ".ot.it", ".pa.it", ".pc.it", ".pd.it", ".pe.it", ".pg.it", ".pi.it", ".pn.it", ".po.it", ".pr.it", ".pt.it", ".pu.it", ".pv.it", ".pz.it", ".ra.it", ".rc.it", ".re.it", ".rg.it", ".ri.it", ".rm.it", ".rn.it", ".ro.it", ".sa.it", ".si.it", ".so.it", ".sp.it", ".sr.it", ".ss.it", ".sv.it", ".ta.it", ".te.it", ".tn.it", ".to.it", ".tp.it", ".tr.it", ".ts.it", ".tv.it", ".ud.it", ".va.it", ".vb.it", ".vc.it", ".ve.it", ".vi.it", ".vr.it", ".vs.it", ".vt.it", ".vv.it", ".co.je", ".jetzt", ".co.jp", ".gr.jp", ".ne.jp", ".or.jp", ".ac.ke", ".co.ke", ".go.ke", ".me.ke", ".ne.ke", ".or.ke", ".sc.ke", ".tm.km", ".koeln", ".co.kr", ".go.kr", ".ms.kr", ".ne.kr", ".or.kr", ".pe.kr", ".re.kr", ".kyoto", ".lamer", ".co.lc", ".lease", ".legal", ".lexus", ".lilly", ".lipsy", ".loans", ".locus", ".lotte", ".lotto", ".co.ls", ".id.lv", ".id.ly", ".ac.ma", ".co.ma", ".mango", ".tm.mc", ".media", ".co.mg", ".tm.mg", ".miami", ".money", ".movie", ".co.ms", ".ac.mu", ".co.mu", ".or.mu", ".music", ".ac.mw", ".co.mw", ".co.mz", ".cc.na", ".co.na", ".nexus", ".ac.ni", ".co.ni", ".in.ni", ".nikon", ".ninja", ".co.nl", ".co.no", ".gs.no", ".nokia", ".nowtv", ".co.nu", ".ac.nz", ".co.nz", ".co.om", ".omega", ".osaka", ".paris", ".parts", ".party", ".phone", ".photo", ".pizza", ".pc.pl", ".tm.pl", ".place", ".co.pn", ".poker", ".at.pr", ".ch.pr", ".de.pr", ".eu.pr", ".fr.pr", ".it.pr", ".nl.pr", ".uk.pr", ".praxi", ".press", ".prime", ".promo", ".co.pt", ".quest", ".radio", ".rehab", ".reise", ".ricoh", ".co.ro", ".ne.ro", ".nt.ro", ".or.ro", ".sa.ro", ".tm.ro", ".rocks", ".rodeo", ".co.rs", ".in.rs", ".pp.ru", ".rugby", ".ac.rw", ".co.rw", ".salon", ".sener", ".seven", ".sharp", ".shell", ".shoes", ".ae.si", ".at.si", ".cn.si", ".co.si", ".de.si", ".uk.si", ".us.si", ".skype", ".sling", ".smart", ".smile", ".solar", ".space", ".sport", ".co.ss", ".me.ss", ".stada", ".store", ".study", ".style", ".sucks", ".swiss", ".co.sz", ".tatar", ".ac.th", ".co.th", ".in.th", ".or.th", ".tires", ".tirol", ".ac.tj", ".co.tj", ".go.tj", ".my.tj", ".tmall", ".today", ".tokyo", ".tools", ".toray", ".total", ".tours", ".av.tr", ".dr.tr", ".tv.tr", ".trade", ".trust", ".co.tt", ".tunes", ".tushu", ".ac.tz", ".co.tz", ".go.tz", ".me.tz", ".ne.tz", ".or.tz", ".sc.tz", ".tv.tz", ".ck.ua", ".cn.ua", ".co.ua", ".cv.ua", ".dn.ua", ".dp.ua", ".if.ua", ".in.ua", ".kh.ua", ".km.ua", ".kr.ua", ".ks.ua", ".lg.ua", ".lt.ua", ".mk.ua", ".od.ua", ".pl.ua", ".pp.ua", ".rv.ua", ".sm.ua", ".te.ua", ".uz.ua", ".vn.ua", ".zp.ua", ".zt.ua", ".ubank", ".ac.ug", ".co.ug", ".go.ug", ".ne.ug", ".or.ug", ".sc.ug", ".ac.uk", ".co.uk", ".me.uk", ".co.uz", ".co.ve", ".vegas", ".co.vi", ".video", ".ac.vn", ".vodka", ".volvo", ".wales", ".watch", ".weber", ".weibo", ".works", ".world", ".xerox", ".yahoo", ".co.za", ".co.zm", ".co.zw", ".\u05d9\u05e9\u05e8\u05d0\u05dc", ".\u0627\u06cc\u0631\u0627\u0646", ".\u0628\u0627\u0632\u0627\u0631", ".\u0628\u06be\u0627\u0631\u062a", ".\u0633\u0648\u062f\u0627\u0646", ".\u0633\u0648\u0631\u064a\u0629", ".\u0647\u0645\u0631\u0627\u0647", ".\u092d\u093e\u0930\u094b\u0924", ".\u0938\u0902\u0917\u0920\u0928", ".\u09ac\u09be\u0982\u09b2\u09be", ".\u0c2d\u0c3e\u0c30\u0c24\u0c4d", ".\u0d2d\u0d3e\u0d30\u0d24\u0d02", ".\u5609\u91cc\u5927\u9152\u5e97", ".\u500b\u4eba.\u9999\u6e2f", ".\u516c\u53f8.\u9999\u6e2f", ".\u653f\u5e9c.\u9999\u6e2f", ".\u6559\u80b2.\u9999\u6e2f", ".\u7d44\u7e54.\u9999\u6e2f", ".\u7db2\u7d61.\u9999\u6e2f", ".aarp", ".able", ".aero", ".akdn", ".ally", ".amex", ".arab", ".army", ".arpa", ".arte", ".asda", ".asia", ".audi", ".auto", ".baby", ".band", ".bank", ".bbva", ".beer", ".best", ".bike", ".bing", ".blog", ".blue", ".bofa", ".bond", ".book", ".buzz", ".cafe", ".call", ".camp", ".care", ".cars", ".casa", ".case", ".cash", ".cbre", ".cern", ".chat", ".citi", ".city", ".club", ".cool", ".coop", ".cyou", ".data", ".date", ".dclk", ".deal", ".dell", ".desi", ".diet", ".dish", ".docs", ".dvag", ".erni", ".fage", ".fail", ".fans", ".farm", ".fast", ".fido", ".film", ".fire", ".fish", ".flir", ".food", ".ford", ".free", ".fund", ".game", ".gbiz", ".gent", ".ggee", ".gift", ".gmbh", ".gold", ".golf", ".goog", ".guge", ".guru", ".hair", ".haus", ".hdfc", ".help", ".here", ".host", ".hsbc", ".icbc", ".ieee", ".imdb", ".immo", ".info", ".itau", ".java", ".jeep", ".jobs", ".jprs", ".kddi", ".kids", ".kiwi", ".kpmg", ".kred", ".land", ".l.lc", ".p.lc", ".lego", ".lgbt", ".lidl", ".life", ".like", ".limo", ".link", ".live", ".loan", ".love", ".ltda", ".luxe", ".maif", ".meet", ".meme", ".menu", ".mini", ".mint", ".mobi", ".moda", ".moto", ".name", ".navy", ".news", ".next", ".i.ng", ".nico", ".nike", ".ollo", ".open", ".page", ".pars", ".pccw", ".pics", ".ping", ".pink", ".play", ".plus", ".pohl", ".porn", ".post", ".prod", ".prof", ".qpon", ".read", ".reit", ".rent", ".rest", ".rich", ".room", ".rsvp", ".ruhr", ".safe", ".sale", ".sarl", ".save", ".saxo", ".scot", ".seat", ".seek", ".sexy", ".shia", ".shop", ".show", ".silk", ".sina", ".site", ".skin", ".sncf", ".sohu", ".song", ".sony", ".spot", ".star", ".surf", ".talk", ".taxi", ".team", ".tech", ".teva", ".tiaa", ".tips", ".town", ".toys", ".tube", ".vana", ".visa", ".viva", ".vivo", ".vote", ".voto", ".wang", ".weir", ".wien", ".wiki", ".wine", ".work", ".xbox", ".yoga", ".zara", ".zero", ".zone", ".\u0434\u0435\u0442\u0438", ".\u0441\u0430\u0439\u0442", ".\u0628\u0627\u0631\u062a", ".\u0628\u064a\u062a\u0643", ".\u062a\u0648\u0646\u0633", ".\u0634\u0628\u0643\u0629", ".\u0639\u0631\u0627\u0642", ".\u0639\u0645\u0627\u0646", ".\u0645\u0648\u0642\u0639", ".\u0680\u0627\u0631\u062a", ".\u092d\u093e\u0930\u0924", ".\u09ad\u09be\u09b0\u09a4", ".\u09ad\u09be\u09f0\u09a4", ".\u0a2d\u0a3e\u0a30\u0a24", ".\u0aad\u0abe\u0ab0\u0aa4", ".\u0b2d\u0b3e\u0b30\u0b24", ".\u0cad\u0cbe\u0cb0\u0ca4", ".\u0dbd\u0d82\u0d9a\u0dcf", ".\u30a2\u30de\u30be\u30f3", ".\u30af\u30e9\u30a6\u30c9", ".\u30b0\u30fc\u30b0\u30eb", ".\u30dd\u30a4\u30f3\u30c8", ".\u7ec4\u7ec7\u673a\u6784", ".\u96fb\u8a0a\u76c8\u79d1", ".\u9999\u683c\u91cc\u62c9", ".aaa", ".abb", ".abc", ".aco", ".ads", ".aeg", ".afl", ".aig", ".anz", ".aol", ".app", ".art", ".aws", ".axa", ".bar", ".bbc", ".bbt", ".bcg", ".bcn", ".bet", ".bid", ".bio", ".biz", ".bms", ".bmw", ".bom", ".boo", ".bot", ".box", ".buy", ".bzh", ".cab", ".cal", ".cam", ".car", ".cat", ".cba", ".cbn", ".ceo", ".cfa", ".cfd", ".com", ".cpa", ".crs", ".dad", ".day", ".dds", ".dev", ".dhl", ".diy", ".dnp", ".dog", ".dot", ".dtv", ".dvr", ".eat", ".eco", ".edu", ".esq", ".eus", ".fan", ".fit", ".fly", ".foo", ".fox", ".frl", ".ftr", ".fun", ".fyi", ".gal", ".gap", ".gay", ".gdn", ".gea", ".gle", ".gmo", ".gmx", ".goo", ".gop", ".got", ".gov", ".hbo", ".hiv", ".hkt", ".hot", ".how", ".ibm", ".ice", ".icu", ".ifm", ".inc", ".ing", ".ink", ".int", ".ist", ".itv", ".jcb", ".jio", ".jll", ".jmp", ".jnj", ".jot", ".joy", ".kfh", ".kia", ".kim", ".kpn", ".krd", ".lat", ".law", ".lds", ".llc", ".llp", ".lol", ".lpl", ".ltd", ".man", ".map", ".mba", ".med", ".men", ".mil", ".mit", ".mlb", ".mls", ".mma", ".moe", ".moi", ".mom", ".mov", ".msd", ".mtn", ".mtr", ".nab", ".nba", ".nec", ".net", ".new", ".nfl", ".ngo", ".nhk", ".now", ".nra", ".nrw", ".ntt", ".nyc", ".obi", ".one", ".ong", ".onl", ".ooo", ".org", ".ott", ".ovh", ".pay", ".pet", ".phd", ".pid", ".pin", ".pnc", ".pro", ".pru", ".pub", ".pwc", ".red", ".ren", ".ril", ".rio", ".rip", ".run", ".rwe", ".sap", ".sas", ".sbi", ".sbs", ".scb", ".sew", ".sex", ".sfr", ".ski", ".sky", ".soy", ".spa", ".srl", ".stc", ".tab", ".tax", ".tci", ".tdk", ".tel", ".thd", ".tjx", ".top", ".trv", ".tui", ".tvs", ".ubs", ".uno", ".uol", ".ups", ".vet", ".vig", ".vin", ".vip", ".wed", ".win", ".wme", ".wow", ".wtc", ".wtf", ".xin", ".xxx", ".xyz", ".you", ".yun", ".zip", ".\u0431\u0435\u043b", ".\u043a\u043e\u043c", ".\u043c\u043a\u0434", ".\u043c\u043e\u043d", ".\u043e\u0440\u0433", ".\u0440\u0443\u0441", ".\u0441\u0440\u0431", ".\u0443\u043a\u0440", ".\u049b\u0430\u0437", ".\u0570\u0561\u0575", ".\u05e7\u05d5\u05dd", ".\u0639\u0631\u0628", ".\u0642\u0637\u0631", ".\u0643\u0648\u0645", ".\u0645\u0635\u0631", ".\u0915\u0949\u092e", ".\u0928\u0947\u091f", ".\u0e04\u0e2d\u0e21", ".\u0e44\u0e17\u0e22", ".\u0ea5\u0eb2\u0ea7", ".\u307f\u3093\u306a", ".\u30b9\u30c8\u30a2", ".\u30bb\u30fc\u30eb", ".\u4e2d\u6587\u7f51", ".\u4e9a\u9a6c\u900a", ".\u5929\u4e3b\u6559", ".\u6211\u7231\u4f60", ".\u65b0\u52a0\u5761", ".\u6de1\u9a6c\u9521", ".\u98de\u5229\u6d66", ".ac", ".ad", ".ae", ".af", ".ag", ".ai", ".al", ".am", ".ao", ".aq", ".ar", ".as", ".at", ".au", ".aw", ".ax", ".az", ".ba", ".bb", ".bd", ".be", ".bf", ".bg", ".bh", ".bi", ".bj", ".bm", ".bn", ".bo", ".br", ".bs", ".bt", ".bv", ".bw", ".by", ".bz", ".ca", ".cc", ".cd", ".cf", ".cg", ".ch", ".ci", ".ck", ".cl", ".cm", ".cn", ".co", ".cr", ".cu", ".cv", ".cw", ".cx", ".cy", ".cz", ".de", ".dj", ".dk", ".dm", ".do", ".dz", ".ec", ".ee", ".eg", ".er", ".es", ".et", ".eu", ".fi", ".fj", ".fk", ".fm", ".fo", ".fr", ".ga", ".gb", ".gd", ".ge", ".gf", ".gg", ".gh", ".gi", ".gl", ".gm", ".gn", ".gp", ".gq", ".gr", ".gs", ".gt", ".gu", ".gw", ".gy", ".hk", ".hm", ".hn", ".hr", ".ht", ".hu", ".id", ".ie", ".il", ".im", ".in", ".io", ".iq", ".ir", ".is", ".it", ".je", ".jm", ".jo", ".jp", ".ke", ".kg", ".kh", ".ki", ".km", ".kn", ".kp", ".kr", ".kw", ".ky", ".kz", ".la", ".lb", ".lc", ".li", ".lk", ".lr", ".ls", ".lt", ".lu", ".lv", ".ly", ".ma", ".mc", ".md", ".me", ".mg", ".mh", ".mk", ".ml", ".mm", ".mn", ".mo", ".mp", ".mq", ".mr", ".ms", ".mt", ".mu", ".mv", ".mw", ".mx", ".my", ".mz", ".na", ".nc", ".ne", ".nf", ".ng", ".ni", ".nl", ".no", ".np", ".nr", ".nu", ".nz", ".om", ".pa", ".pe", ".pf", ".pg", ".ph", ".pk", ".pl", ".pm", ".pn", ".pr", ".ps", ".pt", ".pw", ".py", ".qa", ".re", ".ro", ".rs", ".ru", ".rw", ".sa", ".sb", ".sc", ".sd", ".se", ".sg", ".sh", ".si", ".sj", ".sk", ".sl", ".sm", ".sn", ".so", ".sr", ".ss", ".st", ".su", ".sv", ".sx", ".sy", ".sz", ".tc", ".td", ".tf", ".tg", ".th", ".tj", ".tk", ".tl", ".tm", ".tn", ".to", ".tr", ".tt", ".tv", ".tw", ".tz", ".ua", ".ug", ".uk", ".us", ".uy", ".uz", ".va", ".vc", ".ve", ".vg", ".vi", ".vn", ".vu", ".wf", ".ws", ".ye", ".yt", ".za", ".zm", ".zw", ".\u03b5\u03bb", ".\u03b5\u03c5", ".\u0431\u0433", ".\u0435\u044e", ".\u0440\u0444", ".\u10d2\u10d4", ".\u30b3\u30e0", ".\u4e16\u754c", ".\u4e2d\u4fe1", ".\u4e2d\u56fd", ".\u4e2d\u570b", ".\u4f01\u4e1a", ".\u4f5b\u5c71", ".\u4fe1\u606f", ".\u5065\u5eb7", ".\u516b\u5366", ".\u516c\u53f8", ".\u516c\u76ca", ".\u53f0\u6e7e", ".\u53f0\u7063", ".\u5546\u57ce", ".\u5546\u5e97", ".\u5546\u6807", ".\u5609\u91cc", ".\u5728\u7ebf", ".\u5927\u62ff", ".\u5a31\u4e50", ".\u5bb6\u96fb", ".\u5e7f\u4e1c", ".\u5fae\u535a", ".\u6148\u5584", ".\u624b\u673a", ".\u62db\u8058", ".\u653f\u52a1", ".\u653f\u5e9c", ".\u65b0\u95fb", ".\u65f6\u5c1a", ".\u66f8\u7c4d", ".\u673a\u6784", ".\u6e38\u620f", ".\u6fb3\u9580", ".\u70b9\u770b", ".\u79fb\u52a8", ".\u7f51\u5740", ".\u7f51\u5e97", ".\u7f51\u7ad9", ".\u7f51\u7edc", ".\u8054\u901a", ".\u8c37\u6b4c", ".\u8d2d\u7269", ".\u901a\u8ca9", ".\u96c6\u56e2", ".\u98df\u54c1", ".\u9910\u5385", ".\u9999\u6e2f", ".\ub2f7\ub137", ".\ub2f7\ucef4", ".\uc0bc\uc131", ".\ud55c\uad6d"]

def remove_protocol(url):
    """
    Remove the protocol from the URL

    Parameters
    ----------
    url : str
        The URL to remove the protocol

    Returns
    -------
    str
        The URL without the protocol

    Examples
    --------
    >>> remove_protocol('https://www.google.com')
    'www.google.com'
    >>> remove_protocol('http://www.google.com')
    'www.google.com'
    """
    while True:
        _url = url
        # find if exists the protocol
        index1 = _url.lower().split('/')[0].find('http')
        index2 = _url.lower().split('/')[0].find('www.')
        if index1 != -1:
            _url = _url[index1:]
        elif index2 != -1:
            _url = _url[index2:]
        if index1 == -1 and index2 == -1:
            break
        # remove the protocol
        if _url.lower().startswith('https://'):
            _url = _url[8:]
        elif _url.lower().startswith('http://'):
            _url = _url[7:]
        if _url == url:
            break
        url = _url
    if _url == '':
        return None
    return _url

def get_apex(url_removed_protocol=None):
    if not isinstance(url_removed_protocol, str):
        return None
    apex = url_removed_protocol.split('/')[0].lower().split(':')[0]
    if apex == '':
        return None
    return apex

def split_apex(apex=None, tlds=tlds):
    """
    Split the apex into second, first and tld

    Parameters
    ----------
    apex : str
        The apex to split
    tlds : list
        The list of TLDs

    Returns
    -------
    tuple
        The second, first and tld

    Examples
    --------
    >>> split_apex('www.google.com')
    ('www', 'google', 'com')
    >>> split_apex('www.google.co.uk')
    ('www', 'google', 'co.uk')
    >>> split_apex('google.com')
    (None, 'google', 'com')
    >>> split_apex('google.co.uk')
    (None, 'google', 'co.uk')
    """
    if not isinstance(apex, str):
        return None, None, None
    second, first, tld = None, None, None
    radix = None
    for tld in sorted(tlds, key=len, reverse=True):
        if apex.endswith(tld):
            radix = apex[:-len(tld)]
            tld = tld.strip('.')
            break
    if radix is None:
        return None, None, None
    if radix.count('.') > 0:
        second = '.'.join(radix.split('.')[:-1])
    first = radix.split('.')[-1]
    if second == '':
        second = None
    if first == '':
        first = None
    if tld == '':
        tld = None
    return second, first, tld

def get_path(url_removed_protocol=None):
    """
    Get the path from the URL

    Parameters
    ----------
    url_removed_protocol : str
        The URL without the protocol

    Returns
    -------
    str
        The path

    Examples
    --------
    >>> get_path('www.google.com')
    None
    >>> get_path('www.google.com/')
    None
    >>> get_path('www.google.com/search')
    'search'
    >>> get_path('www.google.com/search/')
    'search'
    """
    if not isinstance(url_removed_protocol, str):
        return None
    path = '/'.join(url_removed_protocol.split('/')[1:]).split('?')[0].strip('/')
    if path == '':
        return None
    return path

def get_extension(path=None):
    """
    Get the extension from the path

    Parameters
    ----------
    path : str
        The path

    Returns
    -------
    str
        The extension

    Examples
    --------
    >>> get_extension('search')
    None
    >>> get_extension('search.html')
    'html'
    >>> get_extension('search.html?query=python')
    'html'
    >>> get_extension('search.html#python')
    'html'
    """
    if not isinstance(path, str):
        return None
    tail = path.split('/')[-1]
    if '.' not in tail:
        return None
    extension = tail.split('.')[-1].lower()
    if extension == '':
        return None
    return extension

def get_query(url_removed_protocol=None):
    """
    Get the query from the URL

    Parameters
    ----------
    url_removed_protocol : str
        The URL without the protocol

    Returns
    -------
    str
        The query

    Examples
    --------
    >>> get_query('www.google.com')
    None
    >>> get_query('www.google.com/search')
    None
    >>> get_query('www.google.com/search?query=python')
    'query=python'
    """
    if not isinstance(url_removed_protocol, str):
        return None
    tail = url_removed_protocol.split('/')[-1]
    if '?' not in tail:
        return None
    query = tail.split('?')[1]
    if query == '':
        return None
    return query

def add_url_info(df, url_column, tlds=tlds, prefix=None, suffix=None):
    """
    Add the URL information to the DataFrame

    Parameters
    ----------
    df : DataFrame
        The DataFrame
    url_column : str
        The column with the URLs
    tlds : list
        The list of TLDs

    Returns
    -------
    None

    Examples
    --------
    >>> df = pd.DataFrame({'url': ['https://www.google.com', 'http://www.google.com', 'www.google.com']})
    >>> add_url_info(df, 'url')
    >>> df
                                  url            apex    second      first    tld    path  extension    query
    0          https://www.google.com  www.google.com       www     google    com     NaN        NaN      NaN
    1           http://www.google.com  www.google.com       www     google    com     NaN        NaN      NaN
    2                  www.google.com  www.google.com       www     google    com     NaN        NaN      NaN
    """
    df[f'{prefix+"_" if isinstance(prefix, str) else ""}apex{"_"+suffix if isinstance(suffix, str) else ""}'], \
    df[f'{prefix+"_" if isinstance(prefix, str) else ""}second{"_"+suffix if isinstance(suffix, str) else ""}'], \
    df[f'{prefix+"_" if isinstance(prefix, str) else ""}first{"_"+suffix if isinstance(suffix, str) else ""}'], \
    df[f'{prefix+"_" if isinstance(prefix, str) else ""}tld{"_"+suffix if isinstance(suffix, str) else ""}'], \
    df[f'{prefix+"_" if isinstance(prefix, str) else ""}path{"_"+suffix if isinstance(suffix, str) else ""}'], \
    df[f'{prefix+"_" if isinstance(prefix, str) else ""}extension{"_"+suffix if isinstance(suffix, str) else ""}'], \
    df[f'{prefix+"_" if isinstance(prefix, str) else ""}query{"_"+suffix if isinstance(suffix, str) else ""}'] = zip(*df[url_column].progress_apply(lambda x: get_url_info(x, tlds)))
    # replace None with np.nan only in the new columns
    for column in [f'{prefix+"_" if isinstance(prefix, str) else ""}apex{"_"+suffix if isinstance(suffix, str) else ""}',
                   f'{prefix+"_" if isinstance(prefix, str) else ""}second{"_"+suffix if isinstance(suffix, str) else ""}',
                   f'{prefix+"_" if isinstance(prefix, str) else ""}first{"_"+suffix if isinstance(suffix, str) else ""}',
                   f'{prefix+"_" if isinstance(prefix, str) else ""}tld{"_"+suffix if isinstance(suffix, str) else ""}',
                   f'{prefix+"_" if isinstance(prefix, str) else ""}path{"_"+suffix if isinstance(suffix, str) else ""}',
                   f'{prefix+"_" if isinstance(prefix, str) else ""}extension{"_"+suffix if isinstance(suffix, str) else ""}',
                   f'{prefix+"_" if isinstance(prefix, str) else ""}query{"_"+suffix if isinstance(suffix, str) else ""}']:
        df[column] = df[column].replace({None: np.nan})

def get_url_info(url, tlds=tlds):
    """
    Get the URL information

    Parameters
    ----------
    url : str
        The URL
    tlds : list
        The list of TLDs

    Returns
    -------
    tuple
        The URL normalized, apex, second, first, tld, path, extension and query

    Examples
    --------
    >>> get_url_info('https://www.google.com')
    ('www.google.com', 'www', 'google', 'com', None, None, None)
    >>> get_url_info('http://www.google.com')
    ('www.google.com', 'www', 'google', 'com', None, None, None)
    >>> get_url_info('www.google.com')
    ('www.google.com', 'www', 'google', 'com', None, None, None)
    >>> get_url_info('www.google.com/search/')
    ('www.google.com', 'www', 'google', 'com', 'search', None, None)
    >>> get_url_info('www.google.com/search.html?query=python')
    ('www.google.com', 'www', 'google', 'com', 'search.html', 'html', 'query=python')
    """
    url_removed_protocol = remove_protocol(url)
    apex = get_apex(url_removed_protocol)
    second, first, tld = split_apex(apex, tlds)
    path = get_path(url_removed_protocol)
    extension = get_extension(path)
    query = get_query(url_removed_protocol)
    return apex, second, first, tld, path, extension, query

def is_valid_url(url):
    """
    Check if the URL is valid

    Parameters
    ----------
    url : str
        The URL

    Returns
    -------
    bool
        True if the URL is valid, False otherwise

    Examples
    --------
    >>> is_valid_url('https://www.google.com')
    True
    >>> is_valid_url('http://www.google')
    False
    """
    if not isinstance(url, str):
        return False
    url_removed_protocol = remove_protocol(url)
    apex = get_apex(url_removed_protocol)
    second, first, tld = split_apex(apex)
    if url_removed_protocol is None or apex is None or first is None or tld is None or all(c.isalnum() or c in ['-', '.'] for c in apex) == False: 
        return False
    if second is not None and (not second[0].isalnum() or not second[-1].isalnum()):
        return False
    if first is not None and (not first[0].isalnum() or not first[-1].isalnum()):
        return False
    for cc in ['..', '--', '.-', '-.']:
        if cc in apex:
            return False
    return True

def get_urls(text):
    """
    Get the URLs from the text

    Parameters
    ----------
    text : str
        The text

    Returns
    -------
    list
        The URLs

    Examples
    --------
    >>> get_urls('https://www.google.com')
    ['https://www.google.com']
    >>> get_urls('Hello, this is a test. Visit http://www.google.com or google.com')
    ['http://www.google.com', 'google.com']
    >>> get_urls('Hello, this is a string without valid URLs: googl.e')
    []
    """
    regex = r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)|[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)"
    urls = re.findall(regex, text)
    valid_urls = []
    for url in urls:
        if is_valid_url(url):
            valid_urls.append(url)
    return valid_urls