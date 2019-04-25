// swift-tools-version:4.2
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "SwiftSox",
    products: [ .library( name: "SwiftSox", targets: ["SwiftSox"]), ],
    targets: [
        .target( name: "SwiftSox", dependencies: ["sox"]),
        .testTarget( name: "SwiftSoxTests", dependencies: ["SwiftSox"]),
        //.target( name: "CSox", dependencies: ["sox"]),
        .systemLibrary( name: "sox", pkgConfig: "sox")
    ]
)

