import { window } from "vscode";

export function pickFiles(): Thenable<string[] | undefined> {
  const files = window.showOpenDialog({ filters: { "Python Files": ["py"] } });
  return files.then((uris) => {
    if (uris) {
      return uris.map((uri) => uri.fsPath);
    } else {
      return undefined;
    }
  });
}
