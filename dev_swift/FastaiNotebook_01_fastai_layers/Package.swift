// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "FastaiNotebook_01_fastai_layers",
    products: [
        .library(name: "FastaiNotebook_01_fastai_layers", targets: ["FastaiNotebook_01_fastai_layers"]),
    ],
    dependencies: [
        .package(path: "../FastaiNotebook_00_load_data"),
        .package(url: "https://github.com/mxcl/Path.swift", from: "0.16.1"),
        .package(url: "https://github.com/JustHTTP/Just", from: "0.7.1")
    ],
    targets: [
        .target(
            name: "FastaiNotebook_01_fastai_layers",
            dependencies: ["Just", "Path"]),
    ]
)
