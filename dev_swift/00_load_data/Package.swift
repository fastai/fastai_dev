
// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "00_load_data",
    products: [
        .library(name: "00_load_data", targets: ["00_load_data"]),
    ],
    dependencies: [

        .package(url: "https://github.com/mxcl/Path.swift", from: "0.16.1"),
        .package(url: "https://github.com/JustHTTP/Just", from: "0.7.1")
    ],
    targets: [
        .target(
            name: "00_load_data",
            dependencies: ["Just", "Path"]),
    ]
)
