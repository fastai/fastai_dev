// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "FastaiNotebook_09_optimizer",
    products: [
        .library(name: "FastaiNotebook_09_optimizer", targets: ["FastaiNotebook_09_optimizer"]),
    ],
    dependencies: [
        .package(path: "../FastaiNotebook_00_load_data"),
        .package(path: "../FastaiNotebook_01_matmul"),
        .package(path: "../FastaiNotebook_01a_fastai_layers"),
        .package(path: "../FastaiNotebook_02_fully_connected"),
        .package(path: "../FastaiNotebook_02a_why_sqrt5"),
        .package(path: "../FastaiNotebook_03_minibatch_training"),
        .package(path: "../FastaiNotebook_04_callbacks"),
        .package(path: "../FastaiNotebook_05_anneal"),
        .package(path: "../FastaiNotebook_05b_early_stopping"),
        .package(path: "../FastaiNotebook_06_cuda"),
        .package(path: "../FastaiNotebook_07_batchnorm"),
        .package(path: "../FastaiNotebook_08_data_block"),
        .package(path: "../FastaiNotebook_08a_heterogeneous_dictionary"),
        .package(url: "https://github.com/mxcl/Path.swift", from: "0.16.1"),
        .package(url: "https://github.com/JustHTTP/Just", from: "0.7.1")
    ],
    targets: [
        .target(
            name: "FastaiNotebook_09_optimizer",
            dependencies: ["Just", "Path"]),
    ]
)
