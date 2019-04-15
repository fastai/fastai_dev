// Note: this has been hand edited.

public protocol HetDictKey: Hashable {
    associatedtype ValueType
    static var key: AnyHashable { get }
}


public struct HeterogeneousDictionary {
    private var underlying: [AnyHashable : Any] = [:]
    
    public init() {}
    public init(_ items: [AnyHashable : Any]) {
        self.underlying = items
    }

    public subscript<T: HetDictKey>(key: T) -> T.ValueType? {
        get {
            return underlying[T.key] as! T.ValueType?
        }
        set(newValue) {
            if let v = newValue {
                underlying[T.key] = v as Any
            } else {
                underlying.removeValue(forKey: T.key)
            }
        }
    }
    
    public mutating func merge(
        _ other: HeterogeneousDictionary,
        uniquingKeysWith combine: (Any, Any) throws -> Any) rethrows {
        try self.underlying.merge(other.underlying, uniquingKeysWith: combine)
    }
}

public struct Accuracy: HetDictKey, Equatable {
    public init() {}
    public static var key = Accuracy() as AnyHashable
    public typealias ValueType = Float32
}

public struct LearningRate: HetDictKey, Equatable {
    public init() {}
    public static var key = LearningRate() as AnyHashable
    public typealias ValueType = Float
}

public struct StepCount: HetDictKey, Equatable {
    public init() {}
    public static var key = StepCount() as AnyHashable
    public typealias ValueType = Int
}
