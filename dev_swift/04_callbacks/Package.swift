
// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "04_callbacks",
    products: [
        .library(name: "04_callbacks", targets: ["04_callbacks"]),
    ],
    dependencies: [
        .package(path: "./00_load_data",
        .package(path: "./01_matmul",
        .package(path: "./02_fully_connected",
        .package(path: "./02a_why_sqrt5",
        .package(path: "./03_minibatch_training",
        .package(url: "https://github.com/mxcl/Path.swift", from: "0.16.1"),
        .package(url: "https://github.com/JustHTTP/Just", from: "0.7.1")
    ],
    targets: [
        .target(
            name: "04_callbacks",
            dependencies: ["Just", "Path"]),
    ]
)
