# Keď sa počítač učí čítať Stöckela

### Slovenský teológ na výskumnom pobyte v Palerme — o digitálnych humanitách, starých knihách a novej nádeji pre evanjelické dedičstvo

*Michal Valčo*

---

Keď som začiatkom februára pristál na letisku v Palerme, prvé, čo ma prekvapilo, neboli palmy ani citrusy. Bola to otázka taxikára: „Čo robí slovenský profesor na Sicílii?" Snažil som sa to vysvetliť jednou vetou. Nepodarilo sa mi to. Ani po dvoch. Tak som povedal: „Učím počítač čítať staré knihy." Taxikár prikývol, akoby to bola najnormálnejšia vec na svete, a začal rozprávať o svojej babke, ktorá mu čítavala zo starého breviára. Tým sa náš rozhovor, paradoxne, dostal presne k jadru veci.

## Prečo Palermo?

Na Univerzite v Palerme pôsobí medzinárodný výskumný tím v rámci projektu ITSERR — talianskej časti európskej výskumnej infraštruktúry RESILIENCE, ktorá sa venuje digitálnym nástrojom pre štúdium náboženstva. Tento tím vyvinul sofistikovaný nástroj na automatickú analýzu textov — konkrétne na rozpoznávanie a označovanie citácií v stredovekých právnických rukopisoch kánonického práva. Ich systém dokáže s presnosťou takmer 98 % nájsť a správne zaradiť právnické odkazy v latinských textoch z 12.–13. storočia.

Dostal som dvojtýždňové výskumné štipendium (Transnational Access Fellowship), aby som s týmto tímom spolupracoval na adaptácii ich nástroja pre úplne iný typ textov — pre teologické spisy protestantskej reformácie na území Horného Uhorska, teda dnešného Slovenska.

## Leonard Stöckel ako pilotný projekt

Naším prvým „pokusným materiálom" sú diela Leonarda Stöckela (1510–1560), bardejovského rektora, teológa a jedného z najvýznamnejších šíriteľov luteránskej reformácie v Uhorsku. Stöckel bol žiakom Martina Luthera a Filipa Melanchtona vo Wittenbergu, a jeho latinské aj nemecké spisy sú plné odkazov — na Písmo sväté, na cirkevných otcov, na augsburské vyznanie, na ďalšie reformačné dokumenty. Práve tieto odkazy sú pre historikov a teológov mimoriadne cenné: ukazujú, z akých prameňov Stöckel čerpal, ako argumentoval, koho považoval za autoritu.

Problém? Čítať stovky strán latinského textu zo 16. storočia a ručne hľadať a zapisovať každý jeden odkaz je práca na roky. Keď sa však tento proces dá — aspoň čiastočne — zveriť počítaču, otvára sa úplne nový obzor.

## Ako to funguje?

Predstavte si to takto: Slovenská národná knižnica už pred rokmi odfotografovala tisíce strán Stöckelových diel a sprístupnila ich v digitálnom archíve DIKDA. My tieto fotografie najprv „prečítame" pomocou technológie rozpoznávania textu (OCR) — počítač sa pozrie na obrázok stránky a pokúsi sa rozoznať písmená. To samo o sebe nie je jednoduché, pretože tlač zo 16. storočia vyzerá inak než dnešné knihy: písmeno „s" sa písalo ako „ſ" (dlhé s), skratky boli všade a niektoré texty používajú gotické písmo.

Po vyčistení a normalizácii textu nastupuje kľúčový krok: ľudskí odborníci — historici, teológovia — si sadnú k textu v špeciálnom anotačnom programe a ručne označia vzorku odkazov. „Toto je citát z Matúša 5,3." „Toto je odkaz na Augustína." „Toto je nadpis kapitoly." Tieto ručne označené vzorky sa stanú „kľúčom k odpovedi" — podkladom, z ktorého sa počítač učí.

A potom nastúpi samotná detekcia — šesť rôznych metód pracuje jedna za druhou, každá s inou špecializáciou. Jedna pozná pravidlá, ako vyzerajú biblické citácie. Druhá má slovník skratiek. Tretia si pamätá vzory z tréningových dát. Štvrtá — štatistický model strojového učenia — analyzuje každé slovo v kontexte šiestich okolitých slov a odhaduje pravdepodobnosť, že patrí k odkazu. Piata hľadá štruktúru dokumentu. A šiesta všetky výsledky zlúči.

Výsledkom je text, v ktorom sú automaticky označené a zaradené stovky odkazov — spolu s informáciou, *ktorá metóda* ich našla a *nakoľko si je istá*.

## Čestnosť stroja

A práve tu prichádzame k niečomu, čo považujem za filozoficky a teologicky dôležité. Náš systém netvrdí, že vie všetko. Každé nájdenie zaradí do jednej z troch kategórií:

- **Isté** — viacero metód sa zhodlo a počítač je vysoko presvedčený. Takéto anotácie môžeme publikovať.
- **Interpretačné** — len jedna metóda niečo našla, alebo presvedčenie je stredné. Takéto nálezy sa posielajú ľudskému odborníkovi na overenie.
- **Odložené** — metódy sa nezhodujú, alebo ide o otázku, ktorá vyžaduje teologický úsudok. Počítač tu hovorí: „Na toto nemám — rozhodnite vy."

Toto nie je len technická vlastnosť. Je to vyjadrenie princípu, ktorý nazývame „epistemická skromnosť" — pokora poznania. Stroj musí vedieť povedať „neviem" a „toto nie je moja kompetencia." V dobe, keď umelá inteligencia čoraz viac vstupuje aj do duchovnej a teologickej oblasti, je takýto prístup — myslím si — zásadný.

## Čo to znamená pre cirkev a historikov?

Prakticky: ak sa tento nástroj podarí úspešne prispôsobiť, budeme môcť spracovať tisíce strán reformačných textov spôsobom, ktorý by ručnou prácou trval desaťročia. Predstavte si databázu, kde zadáte „Rímskym 3,28" a okamžite uvidíte každý výskyt tohto verša naprieč celým Stöckelovým dielom — s kontextom, s odkazmi na ďalšie citované pramene, s možnosťou pozrieť si originálnu stránku.

Pre cirkevných historikov to otvára otázky, ktoré doteraz nebolo možné systematicky skúmať: Ako sa menila Stöckelova argumentácia v priebehu jeho kariéry? Ktorých cirkevných otcov citoval najčastejšie? Ako sa jeho citačné vzory líšia od jeho súčasníkov v Bardejove, Prešove či Kežmarku?

Pre evanjelickú cirkev je tu ešte hlbší rozmer. Naše reformačné dedičstvo — spisy, kázne, polemiky, vyznania — je obrovské, no do veľkej miery neprebádané a ťažko prístupné. Digitálne nástroje nám dávajú možnosť sprístupniť toto dedičstvo novým spôsobom: nielen ako naskenované obrázky v archíve, ale ako *prečítané, pochopené a prehľadávateľné* texty.

## Slovensko v európskom kontexte

Jedným z mojich ďalších cieľov je zapojiť Slovensko do siete RESILIENCE ako pozorovateľskú krajinu. Táto európska infraštruktúra spája výskumné inštitúcie z 11 krajín a vytvára zdieľané nástroje pre digitálny výskum náboženstva. Slovensko — s jeho mimoriadne bohatým, no fragmentovaným náboženským dedičstvom naprieč katolíckou, evanjelickou, reformovanou, pravoslávnou a židovskou tradíciou — má čo ponúknuť aj čo získať.

Valné zhromaždenie RESILIENCE v Bologni v máji 2026 bude kľúčovou príležitosťou. A projekt so Stöckelom je konkrétnym dôkazom, že Slovensko nie je len pasívnym príjemcom technológií, ale aktívnym partnerom, ktorý prináša vlastný materiál, vlastné otázky a vlastnú odbornosť.

## Záver

Taxikár v Palerme nevedel, kto bol Leonard Stöckel. Ale vedel, čo to znamená, keď sa staré slová stretajú s novými nástrojmi — jeho babka čítala z breviára, my čítame z digitálnych archívov. Mení sa médium, no otázky zostávajú rovnaké: Čo nám tieto texty hovoria? Komu patria? A ako ich odovzdať ďalším generáciám?

Možno práve tu — na priesečníku starého a nového, medzi Bardejovom a Palermom, medzi pergamenom a algoritmom — sa otvára priestor pre niečo, čo by sme mohli nazvať digitálnou službou dedičstvu viery.

---

*Prof. Michal Valčo pôsobí na Evanjelickej bohosloveckej fakulte Univerzity Komenského v Bratislave. V súčasnosti je na výskumnom pobyte na Università degli Studi di Palermo v rámci projektu ITSERR/RESILIENCE.*
