// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "FastaiNotebook_10_mixup_ls",
    products: [
        .library(name: "FastaiNotebook_10_mixup_ls", targets: ["FastaiNotebook_10_mixup_ls"]),
    ],
dependencies: [
    .package(path: "/home/ubuntu/dev_swift/FastaiNotebook_09_optimizer")
],
targets: [
    .target(
        name: "FastaiNotebook_10_mixup_ls",
        dependencies: ["FastaiNotebook_09_optimizer"]),
    ]
)