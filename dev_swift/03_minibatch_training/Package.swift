
// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "03_minibatch_training",
    products: [
        .library(name: "03_minibatch_training", targets: ["03_minibatch_training"]),
    ],
    dependencies: [
        .package(path: "./00_load_data",
        .package(path: "./01_matmul",
        .package(path: "./02_fully_connected",
        .package(path: "./02a_why_sqrt5",
        .package(url: "https://github.com/mxcl/Path.swift", from: "0.16.1"),
        .package(url: "https://github.com/JustHTTP/Just", from: "0.7.1")
    ],
    targets: [
        .target(
            name: "03_minibatch_training",
            dependencies: ["Just", "Path"]),
    ]
)
