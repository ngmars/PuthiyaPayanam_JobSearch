from .. import userModels as models
from fastapi import HTTPException

def write_links_to_db(
    db,
    current_user,
    link,
    existing_links
):
    """"
        check if link already exists, if so, update the link 
        since one user can have multiple links, we will need to check if 
        they are updating is_cv, is_linkedIn, is_github. If they add other side, we add that as new link
        link_field does not exist, make link_field false in link 

        Args:
            db: Database session
            current_user: The current authenticated user
            link: The link data to be added/updated
            existing_links: List of existing links for the user
        
        Returns:
            models.UserDataLinks: The created/updated UserDataLinks object.

        @Author Nitish Gopinath
    """
    update_flag = False
    boolean_fields = ['is_cv', 'is_linkedIn', 'is_github']
    for link_field in boolean_fields:
        if link[link_field] is not None:
            for existing_link in existing_links:
                if getattr(existing_link, link_field):
                    existing_link.website_link = link["website_link"]
                    db.commit()
                    db.refresh(existing_link)
                    update_flag = True
                    return existing_link
        else: 
            setattr(link, link_field, False)

    if not update_flag:
        new_link = models.UserDataLinks(
            user_id = current_user.id,
            website_link = link.website_link,
            is_cv = link.is_cv,
            is_linkedIn = link.is_linkedIn,
            is_github = link.is_github,
            other_site = link.other_site
        )
        db.add(new_link)
        db.commit()
        db.refresh(new_link)
        return new_link

    raise HTTPException(status_code=400, detail="Something went wrong...who knows what, try again maybe?")