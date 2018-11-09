
# KBQA demo

Wiki knowledge graph question answering demo.

> This project is inspired by [nlquery](https://github.com/ayoungprogrammer/nlquery).

## Install

### Stanford CoreNLP

1. Download [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/download.html) and Chinese language model files.

2. Unzip CoreNLP and Chinese model, and copy Chinese model files ("StanfordCoreNLP-chinese.properties" and "edu" folder ) into the root directory of CoreNLP.

3. Change directory to root folder of CoreNLP,  and start CoreNLP server:
```shell
java -Xmx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -serverProperties StanfordCoreNLP-chinese.properties -port 9000 -timeout 15000 
```

 Visit `http://localhost:9000` and you will see the web UI of CoreNLP.

### Python requirements

Working on python 3.

Install required packages:
```shell
pip3 install -r requirements.txt
```

### Apache Jena (optional)

This project will use online data source (Baidu baike and zhwiki API provided by zhishi.me) by default. If you decide to use your own data source, please set up Sparql data sources first.

You can download [Apache Jena](https://jena.apache.org/index.html) and [OpenKG.cn knowledge graph dump data](http://openkg.cn/).


## Run

Run
```shell
python3 main.py
```
and enter natural language query.
```

Enter query: 谁是周杰伦

Dependence parse tree: 
(IP (NP (PN 谁)) (VP (VC 是) (NP (NR 周杰伦))))

Entity match:
{'subject': '周杰伦'}

周杰伦（Jay Chou），1979年1月18日出生于台湾省新北市，中国台湾流行乐男歌手、音乐人、演员、导演、编剧、监制、商人。2000年发行首张个人专辑《Jay》。2001年发行的专辑《范特西》奠定其融合中西方音乐的风格。2002年举行“The One”世界巡回演唱会。2003年成为美国《时代周刊》封面人物。2004年获得世界音乐大奖中国区最畅销艺人奖。2005年凭借动作片《头文字D》获得台湾电影金马奖、香港电影金像奖最佳新人奖。2006年起连续三年获得世界音乐大奖中国区最畅销艺人奖。2007年自编自导的文艺片《不能说的秘密》获得台湾电影金马奖年度台湾杰出电影奖。2008年凭借歌曲《青花瓷》获得第19届金曲奖最佳作曲人奖。2009年入选美国CNN评出的“25位亚洲最具影响力的人物”；同年凭借专辑《魔杰座》获得第20届金曲奖最佳国语男歌手奖。2010年入选美国《Fast Company》评出的“全球百大创意人物”。2011年凭借专辑《跨时代》再度获得金曲奖最佳国语男歌手奖，并且第4次获得金曲奖最佳国语专辑奖；同年主演好莱坞电影《青蜂侠》。2012年登福布斯中国名人榜榜首。2014年发行华语乐坛首张数字音乐专辑《哎呦，不错哦》。2016年推出专辑《周杰伦的床边故事》。演艺事业外，他还涉足商业、设计等领域。2007年成立杰威尔有限公司。2011年担任华硕笔电设计师并入股香港文化传信集团。周杰伦热心公益慈善，多次向中国内地灾区捐款捐物。2008年捐款援建希望小学。2014年担任中国禁毒宣传形象大使。


Enter query: 姚明的身高是多少

Dependence parse tree: 
(IP
  (NP (DNP (NP (NR 姚明)) (DEG 的)) (NP (NN 身高)))
  (VP (VC 是) (QP (CD 多少))))
  
Entity property match:
{'subject': '姚明', 'property': '身高'}

Corrected property:
身高

229厘米

```

## Customization

Modify `/qa/query_handler.py` to add more question templates.

Modify `/qa/sparql.py` to change data source or add more query types.

Modify `/dict/property_synonyms.txt` to customize synonyms dict.
 
For each line, the words are separated by space and all of the other words will be replaced by the first word.
For example, `子女 女儿 儿子 孩子`, `女儿` `儿子` `孩子` will be replaced by `子女`.













