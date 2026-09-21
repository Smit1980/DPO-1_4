import json,re,unittest,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
D=json.loads((R/"content/lesson.json").read_text(encoding="utf-8-sig"))
class MaterialChecks(unittest.TestCase):
 def test_timing_and_slides(self):
  self.assertEqual([(s["start"],s["end"]) for s in D["sections"]],[(0,20),(20,45),(45,70),(70,90),(90,115),(115,135),(135,155),(155,175),(175,180)])
  for pair in (1,2):self.assertEqual(sum(s["end"]-s["start"] for s in D["sections"] if s["pair"]==pair),90)
  self.assertEqual([x["id"] for s in D["sections"] for x in s["slides"]],list(range(1,31)))
 def test_every_section_has_teaching_material(self):
  for s in D["sections"]:
   self.assertTrue(s["practice"]["input"])
   self.assertTrue(s["practice"]["prompt"])
   self.assertTrue(s["practice"]["fallback"])
   self.assertTrue(s["teacher"]["speech"])
   self.assertTrue(s["teacher"]["silent"])
   self.assertLessEqual(s["practice"]["minutes"],s["end"]-s["start"])
   if s["id"] in {"s3","s4","s5","s6","s7","s8"}: self.assertTrue(s["sources"])
   for sl in s["slides"]:
    for key in ("explanation","example","takeaway"):self.assertGreater(len(sl[key]),20)
 def test_prompts_complete(self):
  batch=sorted((R/"assets/prompts_v3/batches").glob("*.md"))
  self.assertEqual(len(batch),3)
  all_text=""
  for p in batch:
   t=p.read_text(encoding="utf-8")
   self.assertEqual(len(re.findall(r"^## ПРОМПТ \d{3}",t,re.M)),10)
   self.assertEqual(t.count("ВСЕ русские подписи"),10)
   self.assertEqual(t.count("Выделенный пример"),10)
   all_text+=t
  for n in range(1,31):self.assertIn(f"slide_{n:03d}_v2.png",all_text)
  with zipfile.ZipFile(R/"downloads/slide-prompts-v3.zip") as z:
   self.assertEqual(len(z.namelist()),8)
   self.assertIsNone(z.testzip())
 def test_rehearsal_and_docx(self):
  t=(R/"downloads/teacher-narration.txt").read_text(encoding="utf-8")
  self.assertGreater(len(t.split()),8000)
  self.assertIn("Первая пара завершена",t)
  self.assertNotIn("https://",t)
  with zipfile.ZipFile(R/"downloads/teacher-guide.docx") as z:
   self.assertIn("word/document.xml",z.namelist());self.assertIsNone(z.testzip())
 def test_corrections_and_boundaries(self):
  text=json.dumps(D,ensure_ascii=False)
  self.assertIn("согласование требуется уточнить",text)
  self.assertIn("голос",text)
  self.assertIn("солидарно",text)
  self.assertIn("не норма российского права",text)
  self.assertNotIn("если это невозможно",text.lower())
  self.assertNotIn("Presidio",text)
  self.assertNotIn("PDF24",text)
 def test_synthetic_files(self):
  import csv
  with (R/"downloads/synthetic-minimal.csv").open(encoding="utf-8-sig") as f: rows=list(csv.DictReader(f,delimiter=";"))
  self.assertEqual(len(rows),5)
  self.assertEqual(sum(x["Категория"]=="принтер" for x in rows),3)
  from openpyxl import load_workbook
  b=load_workbook(R/"downloads/synthetic-file-layers.xlsx")
  self.assertEqual(b["Скрытый учебный лист"].sheet_state,"hidden")
  self.assertIsNotNone(b["Учебные заявки"]["B3"].comment)
if __name__=="__main__":unittest.main()
