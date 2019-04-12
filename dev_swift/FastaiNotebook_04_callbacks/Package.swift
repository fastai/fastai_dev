// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "FastaiNotebook_04_callbacks",
    products: [
        .library(name: "FastaiNotebook_04_callbacks", targets: ["FastaiNotebook_04_callbacks"]),
    ],
    dependencies: [
        .package(path: "../FastaiNotebook_00_load_data"),
        .package(path: "../FastaiNotebook_01_fastai_layers"),
        .package(path: "../FastaiNotebook_01_matmul"),
        .package(path: "../FastaiNotebook_02_fully_connected"),
        .package(path: "../FastaiNotebook_02a_why_sqrt5"),
        .package(path: "../FastaiNotebook_03_minibatch_training"),
        .package(url: "https://github.com/mxcl/Path.swift", from: "0.16.1"),
        .package(url: "https://github.com/JustHTTP/Just", from: "0.7.1")
    ],
    targets: [
        .target(
            name: "FastaiNotebook_04_callbacks",
            dependencies: ["Just", "Path"]),
    ]
)
