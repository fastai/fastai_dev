from pathlib import Path
import shutil

src = Path('FastaiNotebooks/Sources/FastaiNotebooks')
mods = sorted(list(src.iterdir()))

pkg_tmpl = """
// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "{name}",
    products: [
        .library(name: "{name}", targets: ["{name}"]),
    ],
    dependencies: [
{deps}
        .package(url: "https://github.com/mxcl/Path.swift", from: "0.16.1"),
        .package(url: "https://github.com/JustHTTP/Just", from: "0.7.1")
    ],
    targets: [
        .target(
            name: "{name}",
            dependencies: ["Just", "Path"]),
    ]
)
"""

dep_tmpl = '        .package(path: "./{name}",'

for i,fn in enumerate(mods):
    name = fn.stem
    dst = Path(name)
    dst.mkdir(exist_ok=True)
    deps = '\n'.join(dep_tmpl.format(name=o.stem) for o in mods[:i])
    with (dst/'Package.swift').open('w') as pkg_f:
        pkg_f.write(pkg_tmpl.format(name=name, deps=deps))
    dst_p = dst/'Sources'/name
    dst_p.mkdir(parents=True, exist_ok=True)
    for fc in mods[:i+1]: shutil.copy(fc, dst_p)

