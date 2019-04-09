
// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "02_fully_connected",
    products: [
        .library(name: "02_fully_connected", targets: ["02_fully_connected"]),
    ],
    dependencies: [
        .package(path: "./00_load_data",
        .package(path: "./01_matmul",
        .package(url: "https://github.com/mxcl/Path.swift", from: "0.16.1"),
        .package(url: "https://github.com/JustHTTP/Just", from: "0.7.1")
    ],
    targets: [
        .target(
            name: "02_fully_connected",
            dependencies: ["Just", "Path"]),
    ]
)
