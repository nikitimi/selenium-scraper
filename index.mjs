import fs from "node:fs/promises";

const textURL = new URL("./urls.txt", import.meta.url);
const tuplePythonURL = new URL("./urls.py", import.meta.url);

const buffer = await fs.readFile(textURL);
const urls = buffer.toString().trim().split("\n");

const tuplelified = JSON.stringify(urls).replace("[", "(").replace("]", ")");

fs.writeFile(tuplePythonURL, `urls = ${tuplelified}`);
