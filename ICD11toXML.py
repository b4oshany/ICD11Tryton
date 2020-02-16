#!/usr/bin/env python
# coding: utf-8

# In[41]:


import json
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom


# In[42]:


with open("icd11.json") as fp:
    icd11_data = json.load(fp)


# In[43]:


data = icd11_data['data']


# In[44]:


#n[it for it in data.values() if  not it['isLeaf']]


# In[45]:


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


# In[46]:


datum = data["1D01.Y"]
datum


# In[69]:


def slugit(text):
    return text.replace('.', '-,-', 1).replace('.', '-').replace('-,-', '.')


# In[70]:


def build_data_xml(data):
    tryton_el = Element('tryton')
    data_el = SubElement(tryton_el, 'data')
    for key, datum in data.items():
        record_el = SubElement(data_el, 'record')
        record_el.set('model', 'gnuhealth.pathology')
        record_el.set('id', slugit("health_icd11.{}".format(datum['theCode'])))


        # data_field_keys = [
        #     'id',
        #     'title',
        #     'stemId',
        #     'theCode',
        # ]
        code = datum['theCode']
        field_name_el = SubElement(record_el, 'field')
        field_name_el.set('name', 'name')
        field_name_el.text = datum['title'].replace('{} '.format(code), '')

        field_code_el = SubElement(record_el, 'field')
        field_code_el.set('name', 'code')
        field_code_el.text = code

        field_category_el = SubElement(record_el, 'field')
        field_category_el.set('name', 'category')
        field_category_el.set('ref', slugit('icd11cat{}'.format(datum['chapter'])) )

        field_title_el = SubElement(record_el, 'field')
        field_title_el.set('name', 'active')
        field_title_el.set('eval', 'True')

        field_classifier_el = SubElement(record_el, 'field')
        field_classifier_el.set('name', 'classifier')
        field_classifier_el.text = 'ICD11'
    return tryton_el


# In[71]:


def build_categories_xml(data):
    tryton_el = Element('tryton')
    data_el = SubElement(tryton_el, 'data')
    for key, text in data.items():
        record_el = SubElement(data_el, 'record')
        record_el.set('model', 'gnuhealth.pathology.category')
        record_el.set('id', slugit("icd11cat{}".format(key)))

        field_name_el = SubElement(record_el, 'field')
        field_name_el.set('name', 'name')
        field_name_el.text = text

        field_classifier_el = SubElement(record_el, 'field')
        field_classifier_el.set('name', 'classifier')
        field_classifier_el.text = 'ICD11'
    return tryton_el


# In[72]:


xml_data = build_data_xml(data)
pretty_xml_data = prettify(xml_data)
print(pretty_xml_data)


# In[73]:


tree = ElementTree.ElementTree(ElementTree.fromstring(pretty_xml_data))
tree.write('icd11.xml',encoding="UTF-8",xml_declaration=True)


# In[74]:


categories = { '10': '10 Diseases of the ear or mastoid process',
  '11': '11 Diseases of the circulatory system',
  '12': '12 Diseases of the respiratory system',
  '13': '13 Diseases of the digestive system',
  '14': '14 Diseases of the skin',
  '15': '15 Diseases of the musculoskeletal system or connective tissue',
  '16': '16 Diseases of the genitourinary system',
  '17': '17 Conditions related to sexual health',
  '18': '18 Pregnancy, childbirth or the puerperium',
  '19': '19 Certain conditions originating in the perinatal period',
  '20': '20 Developmental anomalies',
  '21': '21 Symptoms, signs or clinical findings, not elsewhere classified',
  '22': '22 Injury, poisoning or certain other consequences of external causes',
  '23': '23 External causes of morbidity or mortality',
  '24': '24 Factors influencing health status or contact with health services',
  '25': '25 Codes for special purposes',
  '26': '26 Supplementary Chapter Traditional Medicine Conditions - Module I',
  '01': '01 Certain infectious or parasitic diseases',
  '02': '02 Neoplasms',
  '03': '03 Diseases of the blood or blood-forming organs',
  '04': '04 Diseases of the immune system',
  '05': '05 Endocrine, nutritional or metabolic diseases',
  '06': '06 Mental, behavioural or neurodevelopmental disorders',
  '07': '07 Sleep-wake disorders',
  '08': '08 Diseases of the nervous system',
  '09': '09 Diseases of the visual system',
  'V': 'V Supplementary section for functioning assessment',
  'X': 'X Extension Codes' }


# In[75]:


xml_category = build_categories_xml(categories)
pretty_xml_category = prettify(xml_category)
print(pretty_xml_category)


# In[76]:


tree = ElementTree.ElementTree(ElementTree.fromstring(pretty_xml_category))
tree.write('icd11_disease_categories.xml',encoding="UTF-8",xml_declaration=True)



# In[ ]:




