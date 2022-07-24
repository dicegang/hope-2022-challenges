const fs = require("fs");
const { refactor } = require("shift-refactor");
const {
  VariableDeclarationStatement,
  VariableDeclaration,
  VariableDeclarator,
  BindingIdentifier,
  LiteralStringExpression,
  StaticMemberExpression,
  ComputedMemberExpression,
} = require("shift-ast");
const { parseScript } = require("shift-parser");
const jscrewit = require("jscrewit");

const source = fs.readFileSync("io/input.js").toString();
const $script = refactor(source);

function hashCode(str) {
  let hash = 0;
  for (let i = 0, len = str.length; i < len; i++) {
    let chr = str.charCodeAt(i);
    hash = (hash << 5) - hash + chr;
    hash |= 0;
  }
  return hash;
}

const stringIndirectionTable = {};
$script("LiteralStringExpression").replace(({ value }) => {
  const hash = hashCode(value);
  stringIndirectionTable[hash] = value;
  return `table[${hash}]`;
});

$script("StaticMemberExpression").replace(({ object, property }) => {
  const hash = hashCode(property);
  stringIndirectionTable[hash] = property;
  console.log(parseScript(`table[${hash}]`).statements[0].expression);
  return new ComputedMemberExpression({
    object,
    expression: parseScript(`table[${hash}]`).statements[0].expression,
  });
});

const table = refactor("const table = JSON.parse(A);");
table.$("IdentifierExpression[name=A]").replace(
  () =>
    new LiteralStringExpression({
      value: JSON.stringify(stringIndirectionTable),
    })
);
$script.root.statements.unshift(table.get(0));

$script("LiteralNumericExpression").replace(
  ({ value }) =>
    parseScript(jscrewit.encode(value.toString())).statements[0].expression
);

fs.writeFileSync("io/output.js", $script.codegen().toString());
