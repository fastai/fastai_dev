// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "FastaiNotebook_05b_early_stopping",
    products: [
        .library(name: "FastaiNotebook_05b_early_stopping", targets: ["FastaiNotebook_05b_early_stopping"]),
    ],
dependencies: [
    .package(path: "/home/ubuntu/dev_swift/FastaiNotebook_05_anneal")
],
targets: [
    .target(
        name: "FastaiNotebook_05b_early_stopping",
        dependencies: ["FastaiNotebook_05_anneal"]),
    ]
)