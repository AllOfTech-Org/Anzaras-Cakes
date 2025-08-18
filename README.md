# Anzara's Cake Shop - React Application

This is a React conversion of the original HTML website for Anzara's Cake Shop. The application maintains the exact same visual interface and functionality as the original HTML version.

## Features

- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Product Filtering**: Filter cakes by category (All Cakes, Set Price Cake, Customize Cake, Cutie Cakes, Other)
- **Image Modal**: Click on the search icon to view enlarged images
- **Download Functionality**: Download cake images directly
- **Modern UI**: Clean and professional design with smooth animations
- **Social Media Integration**: Links to Facebook and other social platforms

## Installation

1. Make sure you have Node.js installed on your system (version 14 or higher)

2. Install the dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Build for Production

To create a production build:

```bash
npm run build
```

This will create an optimized build in the `build` folder.

## Project Structure

```
src/
├── components/
│   ├── Header.js          # Header component with logo and social links
│   ├── Header.css         # Header styles
│   ├── FeaturedSection.js # Main product section with filtering
│   ├── FeaturedSection.css # Product section styles
│   ├── Footer.js          # Footer component with contact info
│   ├── Footer.css         # Footer styles
│   ├── ImageModal.js      # Modal for enlarged image view
│   └── ImageModal.css     # Modal styles
├── App.js                 # Main application component
├── App.css               # Global styles and CSS imports
├── index.js              # Application entry point
└── index.css             # Basic global styles

public/
├── css/                  # All CSS files from original HTML
├── img/                  # All images from original HTML
└── index.html            # HTML template
```

## Technologies Used

- **React 18**: Modern React with hooks and functional components
- **CSS3**: Custom styling with animations and responsive design
- **Bootstrap**: For responsive grid system and components
- **Font Awesome**: For icons
- **Google Fonts**: Cairo font family

## Key Features Implemented

1. **Product Filtering**: React state management for filtering products by category
2. **Image Modal**: Modal component for viewing enlarged images
3. **Download Functionality**: Direct image download capability
4. **Responsive Design**: Mobile-first approach with Bootstrap grid
5. **Smooth Animations**: CSS transitions and hover effects
6. **Loading Screen**: Preloader animation on app startup

## Browser Compatibility

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contact Information

- **Address**: Badda, Dhaka-1212
- **Phone**: +8801301927872
- **Email**: hello@anzarascakes.com
- **Facebook**: [Anzara Cakes](https://www.facebook.com/AnzaraCakes)

## License

This project is for Anzara's Cake Shop. All rights reserved.

