//import TensorFlow
//import Path
//import FastaiNotebook_08_data_block
import vips
import Foundation

if vips_init("init") != 0 { fatalError("Failed in init vips") }

let queue = DispatchQueue(label: "q", attributes: .concurrent)
let nt = 8
let semaphore = DispatchSemaphore(value: nt)
for i in 0 ..< 15 {
  semaphore.wait()
  queue.async {
    let songNumber = i + 1
    print("Downloading song", songNumber)
    sleep(1) // Download take ~2 sec each
    print("Downloaded song", songNumber)
    semaphore.signal()
  }
}
for _ in (0..<nt) {semaphore.wait()}
print("done")

/*
func readImage(_ path:String)->Mat {
  let cvImg = imread(path)
  return cvtColor(cvImg, nil, ColorConversionCode.COLOR_BGR2RGB)
}
func readResized(_ fn:String)->Mat {
  return resize(readImage(fn), nil, Size(224, 224), 0, 0, InterpolationFlag.INTER_AREA)
}

public protocol Countable { var count:Int {get} }
extension Mat  :Countable {}
extension Array:Countable {}

public extension Sequence where Element:Countable {
  var totalCount:Int { return map({ $0.count }).reduce(0, +) }
}


let path = downloadImagenette(sz:"")
let allNames = fetchFiles(path: path/"train/n03425413", recurse: false, extensions: ["jpeg", "jpg"])
let fNames = Array(allNames[0..<256])
let ns = fNames.map {$0.string}
let imgpath = ns[0]
let cvImg = readImage(imgpath)

func f()->Array<Mat?> {
  var result = Array<Mat?>(repeating: nil, count: ns.count)
  let q = DispatchQueue(label: "q", attributes: .concurrent)
  var lock = pthread_mutex_t()
  let semaphore = DispatchSemaphore(value: 2)
  let c = ns.count
  for i in 0..<10 {
    semaphore.wait()
    print(i)
    DispatchQueue.global().async {
      //result[i] = nil
      //result[i] = transformed
      //if i==0 {print("*** ", i)}
      pthread_mutex_lock(&lock)
      let transformed = readResized(ns[i])
      semaphore.signal()
      pthread_mutex_unlock(&lock)
    }
  }
  print("c")
  semaphore.wait()
  print("d")

  return result
}

//time { _ = ns.map(readResized) }
//time { _ = f() }

let r = f()
print(r[200] ?? "NA")
*/

