interface Site {
  name: string;
}

interface Article {
  title: string;
  slug: string;
  createdAt: string | number | Date;
  content: string;
  category?: { slug: string; name: string };
}

interface Category {
  name: string;
}

export { Site, Article, Category };
