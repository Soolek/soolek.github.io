#!/usr/bin/env dotnet
#:package SixLabors.ImageSharp@3.1.12
#:property PublishAot=false
// Generates gallery thumbnails for _includes/gallery.html.
//
// For every .jpg / .jpeg / .png in the given folder(s) a centre-cropped 600x400 thumbnail named
// <file>_t.<ext> is written next to it (JPEG: quality 82; PNG: best compression). Existing
// thumbnails are skipped unless --force is given. Originals are never modified.
//
// Usage:  dotnet run scripts/make_thumbnails.cs -- assets/images/driver/e46 [more folders] [--force]
// Needs:  .NET 10 SDK (the first run restores SixLabors.ImageSharp via scripts/nuget.config)
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Formats.Jpeg;
using SixLabors.ImageSharp.Formats.Png;
using SixLabors.ImageSharp.Processing;

// Keep in sync with width/height in _includes/gallery.html and `aspect-ratio: 3 / 2` in _sass/_driver.scss.
var size = new Size(600, 400);
const string Suffix = "_t";
// Same set as the extension filter in _includes/gallery.html.
string[] extensions = [".jpg", ".jpeg", ".png"];

bool force = args.Contains("--force");
string[] folders = args.Where(a => a != "--force").ToArray();
if (folders.Length == 0)
{
    Console.Error.WriteLine("usage: dotnet run scripts/make_thumbnails.cs -- <folder> [more folders] [--force]");
    return 2;
}

int failed = 0;
foreach (string folder in folders)
{
    if (!Directory.Exists(folder))
    {
        Console.Error.WriteLine($"error  {folder} is not a directory");
        failed++;
        continue;
    }
    var sources = Directory.EnumerateFiles(folder)
        .Where(p => extensions.Contains(Path.GetExtension(p).ToLowerInvariant()))
        .Where(p => !Path.GetFileNameWithoutExtension(p).EndsWith(Suffix))
        .Order(StringComparer.Ordinal);
    foreach (string src in sources)
    {
        string dst = Path.Combine(folder, Path.GetFileNameWithoutExtension(src) + Suffix + Path.GetExtension(src));
        if (File.Exists(dst) && !force)
        {
            Console.WriteLine($"skip   {dst} (exists)");
            continue;
        }
        try
        {
            MakeThumbnail(src, dst, size);
        }
        catch (Exception e) when (e is IOException or ImageFormatException)
        {
            Console.Error.WriteLine($"error  {src}: {e.Message}");
            failed++;
            continue;
        }
        Console.WriteLine($"wrote  {dst} {new FileInfo(dst).Length / 1024} KB");
    }
}
return failed > 0 ? 1 : 0;

static void MakeThumbnail(string src, string dst, Size size)
{
    using var image = Image.Load(src);
    image.Mutate(x => x.AutoOrient().Resize(new ResizeOptions
    {
        Size = size,
        Mode = ResizeMode.Crop,
        Sampler = KnownResamplers.Lanczos3,
    }));
    image.Metadata.ExifProfile = null;
    image.Metadata.XmpProfile = null;
    image.Metadata.IptcProfile = null;
    if (Path.GetExtension(dst).Equals(".png", StringComparison.OrdinalIgnoreCase))
        image.Save(dst, new PngEncoder { CompressionLevel = PngCompressionLevel.BestCompression });
    else
        image.Save(dst, new JpegEncoder { Quality = 82 });
}
