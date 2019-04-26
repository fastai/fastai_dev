// swift-tools-version:4.2

import PackageDescription

let package = Package(
    name: "SwiftSox",
    products: [ .library( name: "SwiftSox", targets: ["SwiftSox"]), ],
    targets: [
        .target( name: "SwiftSox", dependencies: ["CSox"]),
        .testTarget( name: "SwiftSoxTests", dependencies: ["SwiftSox"]),
        .target( name: "CSox", dependencies: ["sox"]),
        .systemLibrary( name: "sox", pkgConfig: "sox")
    ]
)
