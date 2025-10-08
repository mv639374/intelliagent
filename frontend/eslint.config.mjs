import globals from "globals";
import tseslint from "typescript-eslint";
import pluginReact from "eslint-plugin-react";
import nextPlugin from "@next/eslint-plugin-next";
import prettierConfig from "eslint-config-prettier";

/** @type {import('typescript-eslint').Config} */
export default tseslint.config(
  {
    // Globally ignored files
    ignores: [".next/**", "next-env.d.ts"], // <-- IGNORE auto-generated file
  },
  {
    // Base configuration for all files
    files: ["**/*.{js,mjs,cjs,ts,jsx,tsx}"],
    plugins: {
      "@next/next": nextPlugin,
      react: pluginReact,
    },
    rules: {
      ...nextPlugin.configs.recommended.rules,
      ...nextPlugin.configs["core-web-vitals"].rules,
      ...pluginReact.configs.recommended.rules,
      "react/react-in-jsx-scope": "off", // <-- DISABLE outdated rule
      "react/prop-types": "off", // <-- DISABLE another common noisy rule
    },
    settings: {
      react: {
        version: "detect",
      },
    },
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
  },
  // TypeScript specific configuration
  ...tseslint.configs.recommended,
  // Prettier configuration (must be last)
  prettierConfig,
);
