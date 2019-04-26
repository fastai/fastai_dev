// swift-tools-version:4.2

import PackageDescription

let package = Package(
    name: "SwiftCV",
    products: [ .library( name: "SwiftCV", targets: ["SwiftCV"]), ],
    targets: [
        .target( name: "SwiftCV", dependencies: ["COpenCV"]),
        .testTarget( name: "SwiftCVTests", dependencies: ["SwiftCV"]),
        .target( name: "COpenCV", dependencies: ["opencv4"]),
        .systemLibrary( name: "opencv4", pkgConfig: "opencv4")
    ]
)
