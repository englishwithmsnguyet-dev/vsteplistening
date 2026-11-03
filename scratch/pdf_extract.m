#import <Foundation/Foundation.h>
#import <PDFKit/PDFKit.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        if (argc < 2) return 1;
        NSString *path = [NSString stringWithUTF8String:argv[1]];
        NSURL *url = [NSURL fileURLWithPath:path];
        PDFDocument *doc = [[PDFDocument alloc] initWithURL:url];
        if (!doc) {
            NSLog(@"Failed to open %@", path);
            return 1;
        }
        for (NSUInteger i = 0; i < doc.pageCount; i++) {
            PDFPage *page = [doc pageAtIndex:i];
            printf("=== PAGE %lu ===\n", (unsigned long)(i + 1));
            printf("%s\n", [page.string UTF8String]);
        }
    }
    return 0;
}
