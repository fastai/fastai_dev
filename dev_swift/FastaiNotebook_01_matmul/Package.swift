// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "FastaiNotebook_01_matmul",
    products: [
        .library(name: "FastaiNotebook_01_matmul", targets: ["FastaiNotebook_01_matmul"]),
    ],
    dependencies: [
        .package(path: "../FastaiNotebook_00_load_data"),
        .package(path: "../FastaiNotebook_01_fastai_layers"),
        .package(url: "https://github.com/mxcl/Path.swift", from: "0.16.1"),
        .package(url: "https://github.com/JustHTTP/Just", from: "0.7.1")
    ],
    targets: [
        .target(
            name: "FastaiNotebook_01_matmul",
            dependencies: ["Just", "Path"]),
    ]
)
