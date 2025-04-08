

from unicodedata import category
from asteval import Interpreter
import lxml.etree as ET
# import xml.etree.ElementTree as ET
from typing import Union
from pathlib import Path
from numpy import isin
import pandas as pd
import base64 as base64
import logging as logging

from excel2moodle.core import question
from excel2moodle.core.exceptions import NanException, QNotParsedException
import excel2moodle.core.etHelpers as eth

from excel2moodle.core.globals import XMLTags, TextElements, DFIndex, questionTypes, parserSettings, feedbackStr, feedBElements
from excel2moodle.core import stringHelpers
from excel2moodle.core.question import Picture, Question
import re as re


logger = logging.getLogger(__name__)
svgFolder = Path("../Fragensammlung/Abbildungen_SVG/")

class QuestionParser():
    def __init__(self, question:Question, dataframe:pd.Series):
        self.question:Question = question
        self.df = dataframe
        self.genFeedbacks:list[XMLTags] = []

    def hasPicture(self)->bool:
        """Creates a ``Picture`` object inside ``question``, if the question needs a pic"""

        picKey = self.df.get(DFIndex.PICTURE)
        if picKey != 0 and not pd.isna(picKey):
            if not hasattr(self.question, 'picture'):
                self.question.picture = Picture(picKey, svgFolder, self.question)
            if self.question.picture.ready:
                return True
        return False

    def setMainText(self)->None:
        paragraphs:list[ET._Element]=[TextElements.PLEFT.create()]
        ET.SubElement(paragraphs[0],"b").text = f"ID {self.question.id}"
        text = self.df.get(DFIndex.TEXT)
        pcount = 0
        for t in text:
            if not pd.isna(t):
                pcount +=1
                paragraphs.append(TextElements.PLEFT.create())
                paragraphs[-1].text = t
        self.question.qtextElements = paragraphs
        logger.debug(f"Created main Text {self.question.id} with:{pcount} paragraphs")
        return None
    
    def setBPoints(self)->None:
        """If there bulletPoints are set in the Spreadsheet it creates an unordered List-Element in ``Question.bulletList``"""
        if DFIndex.BPOINTS in self.df.index:
            bps = self.df.get(DFIndex.BPOINTS)
            try:
                bulletList = self.formatBulletList(bps)
            except IndexError as e:
                raise QNotParsedException(f"konnt Bullet Liste {self.question.id} nicht generieren", self.question.id, exc_info=e)
            self.question.bulletList.append(bulletList)
            logger.debug(f"appendet Bullet List {bulletList = }")
        return None

    def formatBulletList(self,bps:str)->ET.Element:
        li:list[str] =stringHelpers.stripWhitespace( bps.split(';'))
        name = []
        var = []
        quant = []
        unit = []
        unorderedList = TextElements.ULIST.create()
        for item in li:
            sc_split = item.split()
            name.append(sc_split[0])
            var.append(sc_split[1])
            quant.append(sc_split[3])
            unit.append(sc_split[4])
        for i in range(0, len(name)):
            num = quant[i].split(',')
            if len(num)==2:
                num_s = f"{str(num[0])},\\!{str(num[1])}~"
            else: num_s = f"{str(num[0])},\\!0~"
            bullet = TextElements.LISTITEM.create()
            bullet.text=(f"{ name[i] }: \\( {var[i]} = {num_s} \\mathrm{{ {unit[i]}  }}\\)\n")
            unorderedList.append(bullet)
        return unorderedList

    def appendToQuestion(self, eleName: str, text:str|DFIndex, txtEle=False, **attribs ):
        t = (self.df.get(text) if isinstance(text, DFIndex) else text)
        if txtEle is False:
            self.tmpEle.append(eth.getElement(eleName, t, **attribs))
        elif txtEle is True:
            self.tmpEle.append(eth.getTextElement(eleName, t, **attribs))

    def appendFromSettings(self, key="standards")->None:
        """Appends 1 to 1 mapped Elements defined in the parserSettings to the element"""
        parser = ["Parser"]
        if isinstance(self, MCQuestionParser):
                parser.append("MCParser")
        elif isinstance(self, NFQuestionParser):
            parser.append("NFParser")
        for p in parser:
            try:
                for k, v in parserSettings[p][key].items():
                    self.appendToQuestion(k, text=v)
            except KeyError as e:
                msg = f"Invalider Input aus den Einstellungen Parser: {type(p) = }"
                logger.error(msg, exc_info=e)
                raise QNotParsedException(msg, self.question.id, exc_info=e)
        return None

    def parse(self, xmlTree: ET._Element|None=None)->None:
        """Parses the Question
        
        Generates an new Question Element stored as ``self.tmpEle:ET.Element``
        if no Exceptions are raised, ``self.tmpEle`` is passed to ``self.question.element``
        """
        self.tmpEle = ET.Element(XMLTags.QUESTION, type = self.question.moodleType)
        # self.tmpEle.set(XMLTags.TYPE, self.question.moodleType)
        self.appendToQuestion(XMLTags.NAME, text=DFIndex.NAME, txtEle=True)
        self.appendToQuestion(XMLTags.ID, text=self.question.id)
        if self.hasPicture() :
            self.tmpEle.append(self.question.picture.element)
        self.tmpEle.append(ET.Element(XMLTags.QTEXT, format = "html"))
        self.appendToQuestion(XMLTags.POINTS, text=str(self.question.points))
        self.appendToQuestion(XMLTags.PENALTY, text="0.3333")
        self.appendFromSettings()
        for feedb in self.genFeedbacks:
            self.tmpEle.append(eth.getFeedBEle(feedb))
        if xmlTree is not None:
            xmlTree.append(self.tmpEle)
        ansList = self.setAnswers()
        self.setMainText()
        self.setBPoints()
        if ansList is not None:
            for ele in ansList:
                self.tmpEle.append(ele)
        logger.info(f"Sucessfully parsed {self.question.id}")
        self.question.element = self.tmpEle
        return None

    def getFeedBEle(self, feedback:XMLTags, text:str|None=None, style: TextElements | None = None)->ET.Element:
        if style is None:
            span = feedBElements[feedback]
        else: 
            span = style.create()
        if text is None:
            text = feedbackStr[feedback]
        ele = ET.Element(feedback, format="html")
        par = TextElements.PLEFT.create()
        span.text = text
        par.append(span)
        ele.append(eth.getCdatTxtElement(par))
        return ele
    
    def setAnswers(self)->list[ET.Element]|None:
        """Needs to be implemented in the type-specific subclasses"""
        return None

    @staticmethod
    def getNumericAnsElement(result:int|float, 
                             tolerance:float = 0.01, 
                             fraction:int|float = 100, 
                             format:str = "moodle_auto_format")->ET.Element:
        """Returns an ``<answer/>`` Element specific for the numerical Question
        The element contains those childs:
            ``<text/>`` which holds the value of the answer
            ``<tolerace/>`` with the *relative* tolerance for the result
            ``<feedback/>`` with general feedback for a true answer
        """

        ansEle:ET.Element = eth.getTextElement(XMLTags.ANSWER, text = str(result), fraction = str(fraction), format = format)
        ansEle.append(eth.getFeedBEle(XMLTags.ANSFEEDBACK, feedbackStr["right1Percent"], TextElements.SPANGREEN))
        tol = abs(round(result*tolerance, 3))
        ansEle.append(eth.getElement(XMLTags.TOLERANCE, text = str(tol)))
        return ansEle

class NFQuestionParser(QuestionParser):
    def __init__(self, *args)->None:
        super().__init__(*args)
        self.genFeedbacks=[XMLTags.GENFEEDB]

    def setAnswers(self)->list[ET.Element]:
        result = self.df.get(DFIndex.RESULT)
        ansEle:list[ET.Element]=[]
        ansEle.append(self.getNumericAnsElement( result = result ))
        return ansEle

class NFMQuestionParser(QuestionParser):
    def __init__(self, question: Question, dataframe: pd.Series):
        super().__init__(question, dataframe)
        self.genFeedbacks=[XMLTags.GENFEEDB]
        self.astEval = Interpreter()

    def setAnswers(self)->None:
        equation = self.df.get(DFIndex.RESULT)
        bps = self.df.get(DFIndex.BPOINTS)
        ansElementsList:list[ET.Element]=[]
        varNames:list[str]= self.getVarsList(bps)
        varsDict, number = self.getVariablesDict(varNames)
        bulletPoints:list[ET.Element] = []
        for n in range(number):
            self._setupAstIntprt(varsDict, n)
            result = self.astEval(equation)
            if isinstance(result, float):
                ansElementsList.append(self.getNumericAnsElement( result = round(result,3) ))
            bpli = self.insertVariablesToBPoints(varsDict, bps, n)
            bulletPoints.append(self.formatBulletList(bpli))
        self.question.answerVariants = ansElementsList
        self.question.bulletList = bulletPoints
        self.setVariants(len(bulletPoints))
        return None

    def setVariants(self, number:int):
        self.question.variants = number
        mvar = self.question.category.maxVariants
        if mvar is None:
            self.question.category.maxVariants = number
        else:
            self.question.category.maxVariants = number if number <= mvar else mvar



    @staticmethod
    def insertVariablesToBPoints(varDict: dict, bulletPoints: str, index: int)-> str:
        """
        Für jeden Eintrag im varDict, wird im bulletPoints String der Substring "{key}" durch value[index] ersetzt
        """
        for k, v in varDict.items():
            s = r"{" + str(k) + r"}"
            matcher = re.compile(s)
            bulletPoints = matcher.sub(str(v[index]), bulletPoints)
        return bulletPoints

    def _setupAstIntprt(self, var:dict[str, list[str]], index:int)->None:
        """Ubergibt die Parameter mit entsprechenden Variablen-Namen an den asteval-Interpreter.

        Dann kann dieser die equation lesen.
        """
        for k,v in var.items():
            comma = re.compile(r",")
            value = comma.sub(".",v[index])
            self.astEval.symtable[k] = float(value)
        return None

    def getVariablesDict(self, keyList: list)-> tuple[dict[str,list[str]],int]:
        """Liest alle Variablen-Listen deren Name in ``keyList`` ist aus dem DataFrame im Column[index]"""
        dic:dict = {}
        num:int = 0
        for k in keyList:
            val = self.df.get(k)
            if isinstance(val, str)  :
                li = val.split(";")
                num = len(li)
                dic[str(k)] = li
            else: 
                dic[str(k)] = [str(val)]
                num = 1
        print(f"Folgende Variablen wurden gefunden:\n{dic}\n")
        return dic, num

    @staticmethod
    def getVarsList(bps: str|list[str])->list:
        """
        Durchsucht den bulletPoints String nach den Variablen, die als "{var}" gekennzeichnet sind
        """
        vars = []
        if isinstance(bps, list):
            for p in bps:
                vars.extend(re.findall(r"\{\w\}", str(bps)))
        else:
            vars = re.findall(r"\{\w\}", str(bps))
        variablen=[]
        for v in vars:
            variablen.append(v.strip("{}"))
        return variablen

class MCQuestionParser(QuestionParser):
    def __init__(self, *args)->None:
        super().__init__(*args)
        self.genFeedbacks=[
            XMLTags.CORFEEDB,
            XMLTags.PCORFEEDB,
            XMLTags.INCORFEEDB,
            ]

    def getAnsElementsList(self, answerList:list, fraction:float=50, format="html")->list[ET.Element]:
        elementList: list[ET.Element] = []
        for ans in answerList:
            p = TextElements.PLEFT.create()
            p.text = str(ans)
            text = eth.getCdatTxtElement(p)
            elementList.append(ET.Element(XMLTags.ANSWER, fraction=str(fraction), format=format))
            elementList[-1].append(text)
            if fraction < 0:
                elementList[-1].append(eth.getFeedBEle(XMLTags.ANSFEEDBACK, 
                                                        text = feedbackStr["wrong"], 
                                                        style = TextElements.SPANRED))
            elif fraction > 0:
                elementList[-1].append(eth.getFeedBEle(XMLTags.ANSFEEDBACK, 
                                                        text=feedbackStr["right"], 
                                                        style=TextElements.SPANGREEN))
        return elementList


    def setAnswers(self)->list[ET.Element]:
        ansStyle = self.df.get(DFIndex.ANSTYPE)
        true = stringHelpers.stripWhitespace(self.df.get(DFIndex.TRUE).split(';'))
        trueAnsList = stringHelpers.texWrapper(true, style=ansStyle)
        false = stringHelpers.stripWhitespace(self.df.get(DFIndex.FALSE).split(';'))
        falseAnsList= stringHelpers.texWrapper(false, style=ansStyle)
        truefrac = 1/len(trueAnsList)*100
        falsefrac = 1/len(trueAnsList)*(-100)
        self.tmpEle.find(XMLTags.PENALTY).text=str(round(truefrac/100, 4))
        ansList = self.getAnsElementsList(trueAnsList, fraction=round(truefrac, 4))
        ansList.extend(self.getAnsElementsList(falseAnsList, fraction=round(falsefrac, 4)))
        return ansList

