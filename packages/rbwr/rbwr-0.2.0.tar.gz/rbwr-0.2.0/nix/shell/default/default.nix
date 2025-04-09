# Keep sorted.
{
  engage,
  findutils,
  markdownlint-cli,
  mkShell,
  pyright,
  python313,
  reuse,
  ruff,
  uv,
}:

mkShell {
  # Keep sorted.
  packages = [
    engage
    findutils
    markdownlint-cli
    pyright
    python313
    reuse
    ruff
    uv
  ];
}
