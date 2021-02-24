function transformImportCSSM(babel) {
  const { types: t } = babel;

  return {
    name: "transform-import-cssm",
    visitor: {
      ImportDeclaration(path) {
        if (!path.node.source.value.endsWith('.cssm')) {
          return;
        }
        const importName = path.node.specifiers[0].local.name;
        const realName = `_${importName}`;
        path.node.specifiers[0].local.name = realName;
        path.replaceWithMultiple([
          path.node,
          t.expressionStatement(
            t.assignmentExpression(
              '=',
              t.identifier('document.adoptedStyleSheets'),
              t.identifier(`[...document.adoptedStyleSheets, ${realName}]`)
            )
          ),
          t.variableDeclaration('const',[
            t.variableDeclarator(
              t.identifier(importName),
              t.identifier(`JSON.parse(${realName}.cssRules[${realName}.cssRules.length - 1].style.getPropertyValue('--json'))`)
            )
          ])
        ]);
      }
    }
  };
}
Babel.registerPlugin('transform-import-cssm', transformImportCSSM);