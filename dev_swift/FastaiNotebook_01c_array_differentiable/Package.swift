// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "FastaiNotebook_01c_array_differentiable",
    products: [
        .library(name: "FastaiNotebook_01c_array_differentiable", targets: ["FastaiNotebook_01c_array_differentiable"]),
    ],
    dependencies: [
        .package(path: "../FastaiNotebook_00_load_data"),
        .package(path: "../FastaiNotebook_01_matmul"),
        .package(path: "../FastaiNotebook_01a_fastai_layers"),
        .package(url: "https://github.com/mxcl/Path.swift", from: "0.16.1"),
        .package(url: "https://github.com/JustHTTP/Just", from: "0.7.1")
    ],
    targets: [
        .target(
            name: "FastaiNotebook_01c_array_differentiable",
            dependencies: ["Just", "Path"]),
    ]
)
