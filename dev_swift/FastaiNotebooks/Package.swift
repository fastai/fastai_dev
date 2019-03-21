// swift-tools-version:4.0
import PackageDescription

let package = Package(
    name: "FastaiNotebooks",
    products: [
        .library(name: "FastaiNotebooks", targets: ["FastaiNotebooks"]),
    ],
    dependencies: [
        .package(url: "https://github.com/mxcl/Path.swift", from: "0.16.1"),
        .package(url: "https://github.com/JustHTTP/Just", from: "0.7.1")
    ],
    targets: [
        .target(
            name: "FastaiNotebooks",
            dependencies: ["Just", "Path"]),
    ]
)
