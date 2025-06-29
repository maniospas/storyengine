# PLANS FOR ALL PARSERS

Track 

```cpp
vector<string> global_strings;
unordered_map<string,int> string_to_id;
struct Token {
    int value;
    Var(string val) {
        if not val in string_to_id {
            string_to_id[val] = len(string_to_id);
            global_strings[string_to_id[val]] = val;
        }
        value = string_to_id[val];
    }
};
struct Line {
    int pos;
    vector<Token> tokens; // split on spaces,single special characters other than nubmers,gather strings "..." into one token
};
struct Macro {
    vector<Line> lines;
    vector<string> args;
};
struct State {
    unordered_map<string, Macro> macros;
    unordered_map<string, Token> vars;
    vector<Line> lines;
    string seeking;
} state;

void parse_line(string line) {
    if(seeking.size() && !line.startswith("#")) return;
    if(seeking.size() && line)

    find all "\[var\]" in line and replace them by corresponding vars[var] 
    if line starts with "<" ">" "@" "!" and !parse_condition(line) return;
    if line starts with ">>>" then options=line.split(",")
}
```