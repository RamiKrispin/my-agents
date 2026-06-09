#!/usr/bin/env swift
// generate_qr.swift — produce a QR code PNG using macOS CoreImage.
//
// Usage:
//     swift generate_qr.swift <url> [<out=qr.png>] [<size=1500>] [<ec=H>]
//
// Args:
//   url   (required)  — the string to encode (a URL or any short text).
//   out   (optional)  — output PNG path. Defaults to ./qr.png in the cwd.
//                       If a directory is given, writes qr.png inside it.
//   size  (optional)  — final pixel width/height. Default 1500.
//   ec    (optional)  — error-correction level: L | M | Q | H. Default H.
//
// Zero dependencies — CoreImage's CIQRCodeGenerator ships with macOS.

import Foundation
import CoreImage
import AppKit

func die(_ msg: String) -> Never {
    FileHandle.standardError.write((msg + "\n").data(using: .utf8)!)
    exit(1)
}

let args = CommandLine.arguments
if args.count < 2 || args[1] == "-h" || args[1] == "--help" {
    print("usage: swift generate_qr.swift <url> [<out=qr.png>] [<size=1500>] [<ec=H>]")
    exit(args.count < 2 ? 1 : 0)
}

let url  = args[1]
var out  = args.count > 2 ? args[2] : "qr.png"
let size = args.count > 3 ? (Int(args[3]) ?? 1500) : 1500
let ec   = args.count > 4 ? args[4].uppercased() : "H"

guard ["L", "M", "Q", "H"].contains(ec) else {
    die("error: ec must be one of L, M, Q, H (got \"\(ec)\")")
}

// If `out` is a directory, append qr.png. If it's missing .png, append it.
var isDir: ObjCBool = false
if FileManager.default.fileExists(atPath: out, isDirectory: &isDir), isDir.boolValue {
    out = (out as NSString).appendingPathComponent("qr.png")
}
if !out.hasSuffix(".png") { out += ".png" }

// Verify parent dir exists — don't auto-create deep nested trees.
let parent = (out as NSString).deletingLastPathComponent
if !parent.isEmpty,
   !FileManager.default.fileExists(atPath: parent, isDirectory: &isDir) || !isDir.boolValue {
    die("error: parent directory does not exist: \(parent)")
}

guard let payload = url.data(using: .utf8) else {
    die("error: could not encode url as utf-8")
}

guard let f = CIFilter(name: "CIQRCodeGenerator") else {
    die("error: CIQRCodeGenerator filter not available")
}
f.setValue(payload, forKey: "inputMessage")
f.setValue(ec, forKey: "inputCorrectionLevel")

guard var img = f.outputImage else { die("error: CIQRCodeGenerator returned no image") }

// CIQRCodeGenerator outputs at the QR's native module count (~21–177 modules
// across, depending on payload + EC). Scale to the requested size with nearest
// neighbor so module edges stay crisp.
let nativeWidth = img.extent.width
let scale = max(1, CGFloat(size) / nativeWidth)
img = img.transformed(by: CGAffineTransform(scaleX: scale, y: scale))

let rep = NSCIImageRep(ciImage: img)
let nsImg = NSImage(size: rep.size)
nsImg.addRepresentation(rep)

guard let tiff = nsImg.tiffRepresentation,
      let bm   = NSBitmapImageRep(data: tiff),
      let png  = bm.representation(using: .png, properties: [:]) else {
    die("error: PNG encoding failed")
}

do {
    try png.write(to: URL(fileURLWithPath: out))
} catch {
    die("error: writing \(out): \(error.localizedDescription)")
}

print("wrote \(out) — \(png.count) bytes, \(Int(rep.size.width))×\(Int(rep.size.height)), ec=\(ec), encoding: \(url)")
