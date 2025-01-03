import fs from "node:fs/promises";

const textsURL = new URL("./", import.meta.url);
const tuplePythonURL = new URL("./title_and_url.py", import.meta.url);

const files = await fs.readdir(textsURL);
const textExtension = ".txt";
const textExclusion = ["requirements.txt"];

async function getRecordList() {
  let recordList = [];

  for (const textFilename of files.filter(
    (f) => f.includes(textExtension) && !textExclusion.includes(f)
  )) {
    const targetFileURL = new URL(textFilename, textsURL);
    const buffer = await fs.readFile(targetFileURL);
    const array = buffer.toString().trim().split("\r\n");
    const name = textFilename.replace(textExtension, "");

    recordList = array.reduce((prev, curr, i) => {
      recordList[i] = { ...recordList[i], [name]: curr };
      return prev;
    }, recordList);
  }
  return recordList;
}

const recordList = await getRecordList();
const reference = recordList.map((record) => {
  const [title, url] = Object.entries(record);
  return [title[1], url[1]];
});

const tuplelified = JSON.stringify(reference)
  .replace(/\[/g, "(")
  .replace(/\]/g, ")");

fs.writeFile(tuplePythonURL, `data = ${tuplelified}`);
