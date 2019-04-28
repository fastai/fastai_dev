// swift-tools-version:4.2

import PackageDescription

let package = Package(
    name: "SwiftVips",
    products: [ .library( name: "SwiftVips", targets: ["SwiftVips"]), ],
    targets: [
        .target( name: "SwiftVips", dependencies: ["vips"]),
        //.target( name: "dataload", dependencies: ["vips"]),
        .systemLibrary( name: "vips", pkgConfig: "vips")
    ]
)

