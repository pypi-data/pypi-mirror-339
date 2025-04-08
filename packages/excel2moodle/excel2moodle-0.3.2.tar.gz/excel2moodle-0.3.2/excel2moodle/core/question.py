import logging 
import lxml.etree as ET
from pathlib import Path
import base64 as base64

from excel2moodle.core import category, etHelpers
from excel2moodle.core.globals import XMLTags, TextElements, DFIndex, questionTypes, parserSettings
from excel2moodle.core.exceptions import QNotParsedException


logger = logging.getLogger(__name__)

class Question():
    def __init__(self, category,name:str, number:int, parent=None, qtype:str="type", points:float=0):
        self.category = category
        self.katName = self.category.name
        self.name = name
        self.number = number
        self.parent = parent
        self.qtype: str = qtype
        self.moodleType = questionTypes[qtype]
        self.points = ( points if points is not 0 else self.category.points)
        self.element: ET.Element|None=None
        self.picture:Picture
        self.id:str
        self.qtextElements: list[ET.Element] = []
        self.bulletList: list[ET.Element] = []
        self.answerVariants: list[ET.Element] = []
        self.variants:int|None = None
        self.setID()
        self.standardTags = {
            "hidden":"false"
        }
        logger.debug(f"Question {self.id} is initialized")

    def __repr__(self)->str:
        li:list[str] = []
        li.append(f"Question v{self.category.version}")
        li.append(f'{self.id=}')
        li.append(f'{self.parent=}')
        return "\n".join(li)

    def assemble(self, variant:int=1)->None:
        if self.element is not None:
            mainText = self.element.find(XMLTags.QTEXT)
        else: raise QNotParsedException("Cant assamble, if element is none", self.id)
        if len(self.bulletList)>0:
            self.qtextElements.append(self.bulletList[variant-1])
        if hasattr(self, "picture") and self.picture.ready:
            self.qtextElements.append(self.picture.htmlTag)
            mainText.append(self.picture.element)
        mainText.append(etHelpers.getCdatTxtElement(self.qtextElements))
        self.element.insert(3, mainText)
        if len( self.answerVariants ) > 0:
            self.element.insert(5, self.answerVariants[variant-1])
        return None

    def setID(self, id = 0)->None:
        if id == 0:
            self.id: str = f"{self.category.id}{self.number:02d}"
        else: self.id:str = str(id)

class Picture():
    def __init__(self, picKey:str, imgFolder:Path, question:Question):
        self.pic = picKey
        self.ready:bool = False
        self.question = question
        self.imgFolder = (imgFolder / question.katName).resolve()
        self.htmlTag:ET.Element
        self.path:Path
        self._setPath()
        if hasattr(self, 'picID'):
            self.ready = self.__getImg()

    def _setPath(self):
        if self.pic == 1:
            self.picID = self.question.id
        else:
            selectedPic = self.pic[2:]
            logger.debug(f"got a picture key {selectedPic =}")
            try:
                self.picID = f"{self.question.category.id}{int(selectedPic):02d}"
            except ValueError as e:
                logger.warning(msg=f"Bild-ID konnte aus dem Key: {self.pic = }nicht festgestellt werden", exc_info=e)

    def __getBase64Img(self, imgPath):
        with open(imgPath, 'rb') as img:
            img64 = base64.b64encode(img.read()).decode('utf-8')
        return img64

    def __setImgElement(self, dir:Path, picID:int)->None:
        """gibt das Bild im dirPath mit dir qID als base64 encodiert mit den entsprechenden XML-Tags zurück"""
        self.path:Path = ( dir/ str(picID) ).with_suffix('.svg')
        self.element:ET.Element = ET.Element("file", name=f'{self.path.name}', path='/', encoding='base64')
        self.element.text = self.__getBase64Img(self.path)


    def __getImg(self)->bool:
        try:
            self.__setImgElement(self.imgFolder, int(self.picID))
            self.htmlTag = ET.Element("img", src=f"@@PLUGINFILE@@/{self.path.name}", alt=f"Bild {self.path.name}", width="500")
            return True
        except FileNotFoundError as e:
            logger.warning(msg=f"Bild {self.picID} konnte nicht gefunden werden ", exc_info=e)
            self.element = None
            return False
