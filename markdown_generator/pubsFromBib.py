#!/usr/bin/env python
# coding: utf-8

# # Publications markdown generator for academicpages
# 
# Takes a set of bibtex of publications and converts them for use with [academicpages.github.io](academicpages.github.io). This is an interactive Jupyter notebook ([see more info here](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html)). 
# 
# The core python code is also in `pubsFromBibs.py`. 
# Run either from the `markdown_generator` folder after replacing updating the publist dictionary with:
# * bib file names
# * specific venue keys based on your bib file preferences
# * any specific pre-text for specific files
# * Collection Name (future feature)
# 
# TODO: Make this work with other databases of citations, 
# TODO: Merge this with the existing TSV parsing solution


from pybtex.database.input import bibtex
import pybtex.database.input.bibtex 
from time import strptime
import string
import html
import os
import re

#todo: incorporate different collection types rather than a catch all publications, requires other changes to template
publist = {
    @article{zeng2014nano,
    title={A nano-sized solid acid synthesized from rice hull ash for biodiesel production},
    author={Zeng, Danlin and Liu, Shenglan and Gong, Wanjun and Chen, Hongxiang and Wang, Guanghui},
    journal={Rsc Advances},
    volume={4},
    number={39},
    pages={20535--20539},
    year={2014},
    publisher={Royal Society of Chemistry}
    }

    @inproceedings{he2018fluorescence,
    title={Fluorescence lifetime imaging of microviscosity changes during ER autophagy in live cells},
    author={He, Ying and Samanta, Soham and Gong, Wanjun and Liu, Wufan and Pan, Wenhui and Yang, Zhigang and Qu II, Junle},
    booktitle={Biophotonics and Immune Responses XIII},
    volume={10495},
    pages={65--78},
    year={2018},
    organization={SPIE}
    }

    @article{zeng2013acid,
    title={Acid properties of solid acid from petroleum coke by chemical activation and sulfonation},
    author={Zeng, Danlin and Liu, Shenglan and Gong, Wanjun and Wang, Guanghui and Qiu, Jianghua and Tian, Yongsheng},
    journal={Catalysis Communications},
    volume={40},
    pages={5--8},
    year={2013},
    publisher={Elsevier}
    }

    @article{zeng2015effect,
    title={Effect of surface properties of iron oxide sorbents on hydrogen sulfide removal from odor},
    author={Zeng, Danlin and Liu, Shenglan and Gong, Wanjun and Wang, Guanghui and Qiu, Jianghua and Chen, Hongxiang},
    journal={CLEAN--Soil, Air, Water},
    volume={43},
    number={7},
    pages={975--979},
    year={2015},
    publisher={Wiley Online Library}
    }

    @article{chen2020storm,
    title={STORM imaging of mitochondrial dynamics using a vicinal-dithiol-proteins-targeted probe},
    author={Chen, Bingling and Gong, Wanjun and Yang, Zhigang and Pan, Wenhui and Verwilst, Peter and Shin, Jinwoo and Yan, Wei and Liu, Liwei and Qu, Junle and Kim, Jong Seung},
    journal={Biomaterials},
    volume={243},
    pages={119938},
    year={2020},
    publisher={Elsevier}
    }

    @article{gong2017inhibition,
    title={Inhibition and stabilization: cucurbituril induced distinct effects on the Schiff base reaction},
    author={Gong, Wanjun and Ma, Jun and Zhao, Zhiyong and Gao, Fang and Liang, Feng and Zhang, Haijun and Liu, Simin},
    journal={The Journal of Organic Chemistry},
    volume={82},
    number={6},
    pages={3298--3301},
    year={2017},
    publisher={American Chemical Society}
    }

    @article{gong2020super,
    title={Super-resolution imaging of the dynamic cleavage of intercellular tunneling nanotubes},
    author={Gong, Wanjun and Pan, Wenhui and He, Ying and Huang, Meina and Zhang, Jianguo and Gu, Zhenyu and Zhang, Dan and Yang, Zhigang and Qu, Junle},
    journal={Frontiers of Optoelectronics},
    volume={13},
    pages={318--326},
    year={2020},
    publisher={Higher Education Press}
    }

    @article{xu2020nanoliposomes,
    title={Nanoliposomes Co-Encapsulating Photoswitchable Probe and Photosensitizer for Super-Resolution Optical Imaging and Photodynamic Therapy},
    author={Xu, Hao and Chen, Bingling and Gong, Wanjun and Yang, Zhigang and Qu, Junle},
    journal={Cytometry Part A},
    volume={97},
    number={1},
    pages={54--60},
    year={2020},
    publisher={Wiley Online Library}
    }

    @article{gong2019redefining,
    title={Redefining the photo-stability of common fluorophores with triplet state quenchers: mechanistic insights and recent updates},
    author={Gong, Wanjun and Das, Pintu and Samanta, Soham and Xiong, Jia and Pan, Wenhui and Gu, Zhenyu and Zhang, Jianguo and Qu, Junle and Yang, Zhigang},
    journal={Chemical communications},
    volume={55},
    number={60},
    pages={8695--8704},
    year={2019},
    publisher={Royal Society of Chemistry}
    }

    @article{zeng2014bronsted,
    title={A Br{\o}nsted solid acid synthesized from fly ash for vapor phase dehydration of methanol},
    author={Zeng, Danlin and Liu, Shenglan and Gong, Wanjun and Qiu, Jianghua and Chen, Hongxiang and Wang, Guanghui},
    journal={Fuel},
    volume={119},
    pages={202--206},
    year={2014},
    publisher={Elsevier}
    }

    @article{samanta2019organic,
    title={Organic fluorescent probes for stochastic optical reconstruction microscopy (STORM): Recent highlights and future possibilities},
    author={Samanta, Soham and Gong, Wanjun and Li, Wen and Sharma, Amit and Shim, Inseob and Zhang, Wei and Das, Pintu and Pan, Wenhui and Liu, Liwei and Yang, Zhigang and others},
    journal={Coordination Chemistry Reviews},
    volume={380},
    pages={17--34},
    year={2019},
    publisher={Elsevier}
    }

    @article{gong2014encapsulation,
    title={Encapsulation of bipyridinium guests in cucurbit [10] uril},
    author={Gong, Wanjun and Yang, Xiran and Liu, Simin},
    journal={全国第十七届大环化学暨第九届超分子化学学术研讨会论文摘要集},
    year={2014}
    }

    @article{gong2016cover,
    title={Cover Picture: From Packed “Sandwich” to “Russian Doll”: Assembly by Charge-Transfer Interactions in Cucurbit [10] uril (Chem. Eur. J. 49/2016)},
    author={Gong, Wanjun and Yang, Xiran and Zavalij, Peter Y and Isaacs, Lyle and Zhao, Zhiyong and Liu, Simin},
    journal={Chemistry--A European Journal},
    volume={22},
    number={49},
    pages={17489--17489},
    year={2016},
    publisher={Wiley Online Library}
    }

    @article{he2019dual,
    title={Dual-functional fluorescent molecular rotor for endoplasmic reticulum microviscosity imaging during reticulophagy},
    author={He, Ying and Shin, Jinwoo and Gong, Wanjun and Das, Pintu and Qu, Jinghan and Yang, Zhigang and Liu, Wufan and Kang, Chulhun and Qu, Junle and Kim, Jong Seung},
    journal={Chemical Communications},
    volume={55},
    number={17},
    pages={2453--2456},
    year={2019},
    publisher={Royal Society of Chemistry}
    }

    @article{gong2016cucurbituril,
    title={Cucurbituril-Based Supramolecular Nanoreactors/Catalysts},
    author={Gong, Wanjun and Zhao, Zhiyong and Liu, Simin},
    journal={Progress in Chemistry},
    volume={28},
    number={12},
    pages={1732},
    year={2016}
    }

    @article{liu2014self,
    title={Self-healing supramolecular polymers via host-guest interactions},
    author={Liu, Simin and Gong, Wanjun and Yang, Xiran},
    journal={Current Organic Chemistry},
    volume={18},
    number={15},
    pages={2010--2015},
    year={2014},
    publisher={Bentham Science Publishers}
    }

    @article{zeng2014synthesis,
    title={Synthesis, characterization and acid catalysis of solid acid from peanut shell},
    author={Zeng, Danlin and Liu, Shenglan and Gong, Wanjun and Wang, Guanghui and Qiu, Jianghua and Chen, Hongxiang},
    journal={Applied Catalysis A: General},
    volume={469},
    pages={284--289},
    year={2014},
    publisher={Elsevier}
    }

    @article{gong2016packed,
    title={From Packed “Sandwich” to “Russian Doll”: Assembly by Charge-Transfer Interactions in Cucurbit [10] uril},
    author={Gong, Wanjun and Yang, Xiran and Zavalij, Peter Y and Isaacs, Lyle and Zhao, Zhiyong and Liu, Simin},
    journal={Chemistry--A European Journal},
    volume={22},
    number={49},
    pages={17612--17618},
    year={2016}
    }

    @article{gong2022therapeutic,
    title={Therapeutic gas delivery strategies},
    author={Gong, Wanjun and Xia, Chao and He, Qianjun},
    journal={Wiley Interdisciplinary Reviews: Nanomedicine and Nanobiotechnology},
    volume={14},
    number={1},
    pages={e1744},
    year={2022},
    publisher={John Wiley \& Sons, Inc. Hoboken, USA}
    }

    @article{gong2021thermal,
    title={Thermal-stable blue-red dual-emitting Na2Mg2Si6O15: Eu2+, Mn2+ phosphor for plant growth lighting},
    author={Gong, Wanjun and Luo, Jiabao and Zhou, Weiying and Fan, Jiaqi and Sun, Zishan and Zeng, Senxiang and Pan, Haowen and Zhu, Zhenpeng and Yang, Xixiao and Yu, Zhiqiang and others},
    journal={Journal of Luminescence},
    volume={239},
    pages={118372},
    year={2021},
    publisher={North-Holland}
    }

    @article{gong2021gas,
    title={Gas probes and their application in gas therapy},
    author={Gong, Wan-Jun and Yu, Zhi-Qiang and He, Qian-Jun},
    journal={Chemical Synthesis},
    volume={1},
    number={2},
    pages={N--A},
    year={2021},
    publisher={OAE Publishing Inc.}
    }

    @article{guo2021sulourea,
    title={Sulourea-coordinated Pd nanocubes for NIR-responsive photothermal/H 2 S therapy of cancer},
    author={Guo, Xiaoyang and Liu, Jia and Jiang, Lingdong and Gong, Wanjun and Wu, Huixia and He, Qianjun},
    journal={Journal of Nanobiotechnology},
    volume={19},
    pages={1--14},
    year={2021},
    publisher={BioMed Central}
    }

    @article{gong2022activity,
    title={An activity-based ratiometric fluorescent probe for in vivo real-time imaging of hydrogen molecules},
    author={Gong, Wanjun and Jiang, Lingdong and Zhu, Yanxia and Jiang, Mengna and Chen, Danyang and Jin, Zhaokui and Qin, Shucun and Yu, Zhiqiang and He, Qianjun},
    journal={Angewandte Chemie},
    volume={134},
    number={9},
    pages={e202114594},
    year={2022}
    }

    @article{gong2016cover,
    title={COVER PROFILE},
    author={Gong, W and Yang, X and Zavalij, PY and Isaacs, L},
    journal={Chem. Eur. J},
    volume={22},
    pages={17494--17505},
    year={2016}
    }

    @article{jin2023fe,
    title={Fe-porphyrin: A redox-related biosensor of hydrogen molecule},
    author={Jin, Zhaokui and Zhao, Penghe and Gong, Wanjun and Ding, Wenjiang and He, Qianjun},
    journal={Nano Research},
    volume={16},
    number={2},
    pages={2020--2025},
    year={2023},
    publisher={Tsinghua University Press Beijing}
    }

    @article{guo2021sulourea,
    title={Sulourea-coordinated Pd nanocubes for NIR-responsive photothermal/H},
    author={Guo, Xiaoyang and Liu, Jia and Jiang, Lingdong and Gong, Wanjun and Wu, Huixia and He, Qianjun},
    year={2021}
    }
}

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)


for pubsource in publist:
    parser = bibtex.Parser()
    bibdata = parser.parse_file(publist[pubsource]["file"])

    #loop through the individual references in a given bibtex file
    for bib_id in bibdata.entries:
        #reset default date
        pub_year = "1900"
        pub_month = "01"
        pub_day = "01"
        
        b = bibdata.entries[bib_id].fields
        
        try:
            pub_year = f'{b["year"]}'

            #todo: this hack for month and day needs some cleanup
            if "month" in b.keys(): 
                if(len(b["month"])<3):
                    pub_month = "0"+b["month"]
                    pub_month = pub_month[-2:]
                elif(b["month"] not in range(12)):
                    tmnth = strptime(b["month"][:3],'%b').tm_mon   
                    pub_month = "{:02d}".format(tmnth) 
                else:
                    pub_month = str(b["month"])
            if "day" in b.keys(): 
                pub_day = str(b["day"])

                
            pub_date = pub_year+"-"+pub_month+"-"+pub_day
            
            #strip out {} as needed (some bibtex entries that maintain formatting)
            clean_title = b["title"].replace("{", "").replace("}","").replace("\\","").replace(" ","-")    

            url_slug = re.sub("\\[.*\\]|[^a-zA-Z0-9_-]", "", clean_title)
            url_slug = url_slug.replace("--","-")

            md_filename = (str(pub_date) + "-" + url_slug + ".md").replace("--","-")
            html_filename = (str(pub_date) + "-" + url_slug).replace("--","-")

            #Build Citation from text
            citation = ""

            #citation authors - todo - add highlighting for primary author?
            for author in bibdata.entries[bib_id].persons["author"]:
                citation = citation+" "+author.first_names[0]+" "+author.last_names[0]+", "

            #citation title
            citation = citation + "\"" + html_escape(b["title"].replace("{", "").replace("}","").replace("\\","")) + ".\""

            #add venue logic depending on citation type
            venue = publist[pubsource]["venue-pretext"]+b[publist[pubsource]["venuekey"]].replace("{", "").replace("}","").replace("\\","")

            citation = citation + " " + html_escape(venue)
            citation = citation + ", " + pub_year + "."

            
            ## YAML variables
            md = "---\ntitle: \""   + html_escape(b["title"].replace("{", "").replace("}","").replace("\\","")) + '"\n'
            
            md += """collection: """ +  publist[pubsource]["collection"]["name"]

            md += """\npermalink: """ + publist[pubsource]["collection"]["permalink"]  + html_filename
            
            note = False
            if "note" in b.keys():
                if len(str(b["note"])) > 5:
                    md += "\nexcerpt: '" + html_escape(b["note"]) + "'"
                    note = True

            md += "\ndate: " + str(pub_date) 

            md += "\nvenue: '" + html_escape(venue) + "'"
            
            url = False
            if "url" in b.keys():
                if len(str(b["url"])) > 5:
                    md += "\npaperurl: '" + b["url"] + "'"
                    url = True

            md += "\ncitation: '" + html_escape(citation) + "'"

            md += "\n---"

            
            ## Markdown description for individual page
            if note:
                md += "\n" + html_escape(b["note"]) + "\n"

            if url:
                md += "\n[Access paper here](" + b["url"] + "){:target=\"_blank\"}\n" 
            else:
                md += "\nUse [Google Scholar](https://scholar.google.com/scholar?q="+html.escape(clean_title.replace("-","+"))+"){:target=\"_blank\"} for full citation"

            md_filename = os.path.basename(md_filename)

            with open("../_publications/" + md_filename, 'w', encoding="utf-8") as f:
                f.write(md)
            print(f'SUCESSFULLY PARSED {bib_id}: \"', b["title"][:60],"..."*(len(b['title'])>60),"\"")
        # field may not exist for a reference
        except KeyError as e:
            print(f'WARNING Missing Expected Field {e} from entry {bib_id}: \"', b["title"][:30],"..."*(len(b['title'])>30),"\"")
            continue
