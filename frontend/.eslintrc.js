export default {
  "extends": ["airbnb", "plugin:jest/recommended", "react-app"],
  "parser": "babel-eslint",
  "env": {
    "browser": true,
    "node": true
  },
  "settings": {
    "import/resolver": {
      "node": {
        "moduleDirectory": [
          "node_modules",
          "src"
        ]
      }
    }
  },
  "rules": {
    "indent": ["error", 4],
    "react/jsx-indent": ["error", 4],
    "react/jsx-filename-extension": 0,
    "react/jsx-one-expression-per-line": 0,
    "react/jsx-no-bind": 0,
    "react/destructuring-assignment": 0,
    "react/forbid-prop-types": ["error", {"forbid": ["any"]}],
    "react/require-default-props": 0,
    "react/no-string-refs": 0,
    "react/no-multi-comp": 0,
    "react/no-access-state-in-setstate": 0,
    "jsx-ally/no-static-element-interactions": 0,
    "jsx-ally/click-events-have-key-events": 0,
    "import/prefer-default-export": 0,
    "no-underscore-dangle": 0,
    "no-use-before-define": 0,
    "no-continue": 0,
    "operator-linebreak": 0,
    "array-callback-return": 0,
    "consistent-return": 0,
    "class-methods-use-this": 0,
    "max-len": ["error", {"code": 175}],
    "linebreak-style": 0,
    "lines-between-class-members": 0,
    "camelcase": 0,
    "strict": 0
  }
}