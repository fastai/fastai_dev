// swift-tools-version:4.0
import PackageDescription

let package = Package(
    name: "notebook2script",
    products: [
        .executable(name: "Notebook2Script", targets: ["Notebook2Script"]),
    ],
    dependencies: [
        .package(url: "https://github.com/mxcl/Path.swift", from: "0.16.1"),
    ],
    targets: [
        .target(name: "Notebook2Script", dependencies: ["Path"]),
    ]
)
