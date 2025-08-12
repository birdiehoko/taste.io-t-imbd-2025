import csv
import re

names = []
ratings = []

with open('element.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    line = lines[i].strip()
    # Find name
    name_match = re.match(r'<div class="styles_name__HrQH_ ellipsis">(.*?)</div>', line)
    if name_match:
        name = name_match.group(1)
        names.append(name)
        # Now, look for the next div with class styles_userRating__Pple5
        rating = None
        j = i + 1
        while j < len(lines):
            rating_line = lines[j].strip()
            if rating_line.startswith('<div class="styles_userRating__Pple5"'):
                # Collect all lines until the closing </div> of this rating block
                rating_block = [rating_line]
                open_divs = rating_line.count('<div') - rating_line.count('</div>')
                k = j + 1
                while open_divs > 0 and k < len(lines):
                    l = lines[k].strip()
                    rating_block.append(l)
                    open_divs += l.count('<div') - l.count('</div>')
                    k += 1
                # Join the block and count SVGs without the style color: rgba(255, 255, 255, 0.1);
                block_str = '\n'.join(rating_block)
                # Find all svg tags
                svg_tags = re.findall(r'(<svg[\s\S]*?>)', block_str)
                # For each svg, check if it has the style color: rgba(255, 255, 255, 0.1);
                count = 0
                for svg in svg_tags:
                    if 'style="color: rgba(255, 255, 255, 0.1);"' not in svg:
                        count += 1
                rating = count
                ratings.append(rating)
                i = k - 1  # Move i to the end of the rating block
                break
            j += 1
        if rating is None:
            ratings.append('')
    i += 1

# Write to CSV
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name', 'rating'])
    for name, rating in zip(names, ratings):
        writer.writerow([name, rating])


