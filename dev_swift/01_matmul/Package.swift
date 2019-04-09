
// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "01_matmul",
    products: [
        .library(name: "01_matmul", targets: ["01_matmul"]),
    ],
    dependencies: [
        .package(path: "./00_load_data",
        .package(url: "https://github.com/mxcl/Path.swift", from: "0.16.1"),
        .package(url: "https://github.com/JustHTTP/Just", from: "0.7.1")
    ],
    targets: [
        .target(
            name: "01_matmul",
            dependencies: ["Just", "Path"]),
    ]
)
