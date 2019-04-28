import vips

public func VipsInit() {
  if vips_init("init") != 0 { fatalError("Failed in init vips") }
}

