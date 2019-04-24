// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "FastaiNotebook_00_load_data",
    products: [
        .library(name: "FastaiNotebook_00_load_data", targets: ["FastaiNotebook_00_load_data"]),
    ],
dependencies: [
    .package(url: "https://github.com/mxcl/Path.swift", from: "0.16.1"),
    .package(url: "https://github.com/JustHTTP/Just", from: "0.7.1"),
    .package(url: "https://github.com/latenitesoft/NotebookExport", .branch("fastai"))
],
targets: [
    .target(
        name: "FastaiNotebook_00_load_data",
        dependencies: ["Path", "Just", "NotebookExport"]),
    ]
)