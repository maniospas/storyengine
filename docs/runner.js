/*
Copyright 2025 Emmanouil Krasanakis

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/


function processValue(value, vars) {
    if (value.startsWith("[")) {
        if(!(value in vars)) throw new Error("Variable not found: " + value.slice(1, -1));
        value = vars[value];
    }
    const num = parseInt(value, 10);
    if (!isNaN(num)) return num;
    if (!(value.startsWith("\"") && value.endsWith("\"") && value.length >= 2)) throw new Error("Value should be either a number or a string enclosed in \" but is neither: " + value);
    return value.slice(1, -1);
}

function processVariableName(expr, vars) {
    const prev = expr;
    if (expr.startsWith("[")) {
        expr = processValue(expr, vars);
        if (typeof expr !== "string") throw new Error("Can only obtain names from string values: " + prev);
    }
    return `[${expr}]`;
}

function processVariableValue(expr, vars) {
    expr = processVariableName(expr, vars);
    if (!(expr in vars)) throw new Error("This was previously not set: " + expr);
    return vars[expr];
}

function processCondition(line, vars) {
    if (line.startsWith("!")) {
        const args = line.slice(1).trim().split(" ");
        if (args.length <= 2) throw new Error("Condition `! value var` must be followed by the rest of a line");
        const arg0 = processValue(args[0], vars);
        const arg1 = processVariableValue(args[1], vars);
        if ((typeof arg0 === "number") !== (typeof arg1 === "number"))  throw new Error("`! value var` can only compare both numbers or both strings\nCurrent inputs: " + arg0 + ", " + arg1);
        if (arg0 === arg1) return;
        return processCondition(args.slice(2).join(" "), vars);
    }
    if (line.startsWith("@")) {
        const args = line.slice(1).trim().split(" ");
        if (args.length <= 2) throw new Error("Condition `@ value var` must be followed by the rest of a line");
        const arg0 = processValue(args[0], vars);
        const arg1 = processVariableValue(args[1], vars);
        if ((typeof arg0 === "number") !== (typeof arg1 === "number")) throw new Error("`@ value var` can only compare both numbers or both strings\nCurrent inputs: " + arg0 + ", " + arg1);
        if (arg0 !== arg1) return;
        return processCondition(args.slice(2).join(" "), vars);
    }
    if (line.startsWith(">") && !line.startsWith(">>>")) {
        const args = line.slice(1).trim().split(" ");
        if (args.length <= 2) throw new Error("Condition `> value var` must be followed by the rest of a line: " + args);
        const arg0 = processValue(args[0], vars);
        const arg1 = processVariableValue(args[1], vars);
        if (typeof arg0 !== "number" || typeof arg1 !== "number") throw new Error("`> value var` can only compare numbers\nCurrent inputs: " + arg0 + ", " + arg1);
        if (arg0 >= arg1) return;
        return processCondition(args.slice(2).join(" "), vars);
    }
    if (line.startsWith("<") && !line.startsWith("<<<")) {
        const args = line.slice(1).trim().split(" ");
        if (args.length <= 2) throw new Error("Condition `< value var` must be followed by the rest of a line: " + args);
        const arg0 = processValue(args[0], vars);
        const arg1 = processVariableValue(args[1], vars);
        if (typeof arg0 !== "number" || typeof arg1 !== "number") throw new Error("`< value var` can only compare numbers\nCurrent inputs: " + arg0 + ", " + arg1);
        if (arg0 <= arg1) return;
        return processCondition(args.slice(2).join(" "), vars);
    }
    return line;
}

function processLine(line, vars) {
    line = processCondition(line, vars);
    if (!line) return line;
    if (line.startsWith("=")) {
        const parts = line.slice(1).trim().split(/\s+/);
        if (parts.length !== 2) throw new Error("Wrong syntax: expected `=value varname`");
        vars[processVariableName(parts[1], vars)] = processValue(parts[0], vars);
        return;
    }
    if (line.startsWith("?")) {
        const parts = line.slice(1).trim().split(/\s+/);
        if (parts.length !== 2) throw new Error("Wrong syntax: expected `?value varname`");
        const value = processValue(parts[0], vars);
        if (typeof value !== "number") throw new Error("?value can only be applied on number values");
        const rand = value >= 0
            ? Math.floor(Math.random() * (value + 1))
            : -Math.floor(Math.random() * (-value + 1));
        vars[processVariableName(parts[1], vars)] = rand;
        return;
    }
    const arithmeticOps = {
        "+": (a, b) => a + b,
        "-": (a, b) => a - b,
        "*": (a, b) => a * b,
        "/": (a, b) => a / b
    };
    for (const op of Object.keys(arithmeticOps)) {
        if (line.startsWith(op)) {
            const parts = line.slice(1).trim().split(/\s+/);
            if (parts.length !== 2)  throw new Error(`Wrong syntax: expected \`${op}value varname\``);
            const value = processValue(parts[0], vars);
            const varName = processVariableName(parts[1], vars);
            if (typeof value !== "number") throw new Error(`${op}value can only be applied on number values`);
            if (!(varName in vars)) throw new Error("This was previously not set: " + varName);
            if (typeof vars[varName] !== "number") throw new Error(`${op}value can only be applied on number variables`);
            vars[varName] = arithmeticOps[op](vars[varName], value);
            return;
        }
    }
    if (line.startsWith("^")) {
        let args = line.slice(1).trim().split(" ", 3);
        args = args.map(arg => vars["[" + arg.trim() + "]"] ?? arg.trim());
        if (typeof args[1] !== "string") throw new Error("^ expects a string as second argument");
        line = args[1].repeat(parseInt(args[0], 10));
    }
    for (const [varName, value] of Object.entries(vars)) line = line.replaceAll(varName, String(value));
    return line;
}

function escapeHtml(str) {
    return str;
}


document.getElementById('run-btn').addEventListener('click', async () => {
const out  = document.getElementById('output');
const hud  = document.getElementById('hud');
let current_line = 0;
let file_lines = escapeHtml(document.getElementById('editor').innerText).split('\n');

try{
  out.innerHTML = "";
  const ui = [];
  let vars = {
    "[reset]" : "</span><span>",
    "[red]": "</span><span style='color:#AE1423;'>", 
    "[green]": "</span><span style='color:#1B6339;'>", 
    "[yellow]": "</span><span style='color:#C79A29;'>", 
    "[purple]": "</span><span style='color:#7B3FC6;'>",  
    "[cyan]": "</span><span style='color:#247D8F;'>",    
    "[blue]": "</span><span style='color:#0061FE;'>",     
    "[white]": "</span><span style='color:#dddddd;'>",  
    "[separator]": "<hr>",
    "[__refresh]": "20",
    "[end]": "<br>",
    "[describe_controls]": "Click on options as they appear to progress."
  }

  async function drawUi() {
      let uiLines = 0;
      let accum = "";
      hud.innerHTML = "";

      for (const rawLine of ui) {
          if (rawLine == null) continue;
          const line = processLine(rawLine, vars);
          if (line == null) continue;
          if (line.endsWith("[noend]")) {
              accum += line;
              continue;
          }
          const fullLine = (accum + line).replace(/\[noend\]/g, "");
          const lineEl = document.createElement("div");
          lineEl.innerHTML = fullLine;
          hud.appendChild(lineEl);
          uiLines++;
          accum = "";
      }
      hud.hidden = uiLines === 0;
  }


  async function printWithSkip(text, delay) {
    return new Promise(resolve => {
        let i = 0;
        let buffer = ""; // holds the current output
        const container = document.createElement("span"); // container for typed content
        out.appendChild(container);
        function printNextChar() {
            if (i >= text.length) {
                container.innerHTML += "<br>";
                resolve(false);
                return;
            }
            if (text[i] === "<") {
                let tag = "";
                while (i < text.length && text[i] !== ">") {tag += text[i++];}
                if (i < text.length) tag += text[i++]; // include '>'
                buffer += tag;
                container.innerHTML = buffer;
                printNextChar();
            } else {
                buffer += text[i++];
                container.innerHTML = buffer;
                setTimeout(printNextChar, delay);
            }
        }

        printNextChar();
    });
}



  async function appendToOutput(lines, vars, skipping=false) {
      await drawUi();
      let accum = "";
      for (let i = 0; i < lines.length; i++) {
          let line = lines[i];
          if (line == null) continue;
          if (line.endsWith("[noend]")) {
              accum += line;
              continue;
          }
          let fullText = accum + line;
          let printer = !fullText.startsWith("|") || fullText === "|";
          let outputLine = fullText;
          if(fullText.startsWith("|")) outputLine = fullText.slice(1);
          else if(skipping) printer = false;
          fullText = "<span>"+fullText.replace(/\[noend\]/g, "")+"</span>";
          if (printer) {
              const delay = parseFloat(vars["[__refresh]"]) || 30;
              skipping = await printWithSkip(outputLine, delay);
          } 
          else out.textContent += outputLine + "\n";
          accum = "";
      }
      out.scrollTop = out.scrollHeight;
      return skipping;
  }
  async function waitForUserSelection(options) {
      await drawUi();
      if (options.length === 1) return options[0];
      const outEl = document.getElementById("output");
      const savedNodes = Array.from(outEl.childNodes).map(node => node.cloneNode(true));
      return new Promise(resolve => {
          const optionsContainer = document.createElement("div");
          optionsContainer.className = "inline-options";
          options.forEach(opt => {
              const button = document.createElement("button");
              const tempSpan = document.createElement("span");
              tempSpan.innerHTML = opt; 
              button.innerHTML = tempSpan.innerHTML;
              button.onclick = () => {
                  outEl.innerHTML = "";
                  savedNodes.forEach(node => outEl.appendChild(node));
                  // const echoSpan = document.createElement("span");
                  // echoSpan.innerHTML = `> ${opt}`;
                  // outEl.appendChild(echoSpan);
                  // outEl.appendChild(document.createElement("br"));
                  resolve(opt);
              };

              optionsContainer.appendChild(button);
          });
          outEl.appendChild(optionsContainer);
          out.scrollTop = out.scrollHeight;
      });
  }


  async function waitForContinueButton(label = "Continue") {
      await drawUi();
      const outEl = document.getElementById("output");
      const savedNodes = Array.from(outEl.childNodes).map(node => node.cloneNode(true));
      return new Promise(resolve => {
          const container = document.createElement("div");
          container.className = "inline-options";
          const button = document.createElement("button");
          const tempSpan = document.createElement("span");
          tempSpan.innerHTML = label;
          button.innerHTML = tempSpan.innerHTML; // preserve any HTML formatting
          button.onclick = () => {
              outEl.innerHTML = "";
              savedNodes.forEach(node => outEl.appendChild(node));
              resolve();
          };
          container.appendChild(button);
          outEl.appendChild(container);
          out.scrollTop = out.scrollHeight;
      });
  }





  let restarts = true;
  let waiting_for = "";
  let declaring_macro = "", macros = {}, macro_args = {};
  let declaring_ui = false, ui_component_name = "", ui_components = {};
  let skipping = false;

  while(restarts) {
      restarts = false;
      current_line = 0;
      while(current_line < file_lines.length) {
          let line = file_lines[current_line].trimEnd().trim();
          current_line++;
          if(!line) continue;
          if(declaring_macro) {
              if(line.startsWith("&")) declaring_macro = "";
              else macros[declaring_macro].push(line);
          } 
          else if(line.startsWith("#")) {
              line = line.slice(1).trim();
              if(!line) throw new Error("Unnamed segment");
              if(line) line = processLine(line.trim(), vars);
              if (line === waiting_for || !waiting_for) {
                  waiting_for = "";
                  skipping = false;
              }
          } 
          else if(waiting_for) continue;
          else if(line.startsWith("&")) {
              declaring_macro = processLine(line.slice(1).trim(), vars);
              if(!declaring_macro) throw new Error("Invalid macro declaration");
              declaring_macro = declaring_macro.split(" ");
              macros[declaring_macro[0]] = [];
              macro_args[declaring_macro[0]] = declaring_macro.slice(1);
              declaring_macro = declaring_macro[0];
          } 
          else if(line.startsWith("%")) {
              const uiName = processLine(line.slice(1).trim(), vars);
              if (declaring_ui && uiName) throw new Error("Unexpected UI name inside UI block");
              if (!declaring_ui) {
                  if (ui_components[uiName]) {
                      const [start, end = ui.length] = ui_components[uiName];
                      for (let i = start; i < end; i++) ui[i] = null;
                  }
                  ui_components[uiName] = [ui.length];
              }
              ui_component_name = uiName;
              declaring_ui = !declaring_ui;
          } 
          else if(declaring_ui) ui.push(line);
          else {
              const cond = processCondition(line, vars);
              if (cond == null) continue;
              line = cond;
              if(line.startsWith("`")) {
                  let msg = processLine(line.slice(1).trim(), vars);
                  if (!msg) continue;
                  await waitForContinueButton(`${msg}`);
              } 
              else if(line.startsWith("\\\\")) {
                  let macroLine = processLine(line.slice(2).trim(), vars);
                  if (!macroLine) throw new Error("Empty macro invocation");
                  const spaceIdx = macroLine.indexOf(" ");
                  let macroName, macroParams;
                  if (spaceIdx === -1) {
                      macroName = macroLine;
                      macroParams = [];
                  } 
                  else {
                      macroName = macroLine.slice(0, spaceIdx);
                      macroParams = macroLine.slice(spaceIdx + 1).split(",");
                  }
                  let injected = macros[macroName];
                  if (macroParams.length !== macro_args[macroName].length) throw new Error("Macro arguments mismatch");
                  for (let [arg, val] of macro_args[macroName].map((a, i) => [a, macroParams[i]])) injected = injected.map(text => text.replaceAll(`[${arg}]`, val));
                  file_lines = [...injected, ...file_lines.slice(current_line)];
                  if(!file_lines) throw Error("Failed to inject macro");
                  current_line = 0;
              } 
              else if(line.startsWith("<<<") || line.startsWith(">>>")) {
                  const restartMode = line.startsWith("<<<");
                  waiting_for = processLine(line.slice(3).trim(), vars);
                  waiting_for_origin = file_lines[current_line];
                  if (!waiting_for) {
                      out.innerHTML = "";
                      continue;
                  }
                  const options = waiting_for.split(",");
                  waiting_for = await waitForUserSelection(options);
                  if(!waiting_for) throw new Error("Failed to select");
                  if (restartMode) {
                      restarts = true;
                      out.innerHTML = "";
                      break;
                  }
              } 
              else {
                  const processed = processLine(line, vars);
                  if (processed != null) for (const subline of processed.split("\n")) {
                      await appendToOutput([subline], vars, skipping=false);
                  }
              }
          }
      }
  }


}catch(error){
out.innerHTML = "<b>"+error+"</b><br><br>At line "+(current_line-1)+":<br>"+file_lines[current_line-1];
hud.innerHTML = "";
document.getElementById("options").innerHTML = "";
}});
